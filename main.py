#
# Fractals.py
# Creating recursive geometries with tkinter
#
# Jonatan H Sundqvist
# August 13 2014
#

# TODO | - Other fractal types (Koch, Mandelbrot, etc.)
#		 -

# SPEC | -
#		 -


import tkinter as tk
import math
from Graphics import π, RAD, DEG, rect, polar
from collections import namedtuple
from itertools import count
from random import random


Context = namedtuple('Context', 'window, canvas')
Branch  = namedtuple('Branch', 'beg end depth')
# TODO: Include angle in Branch (?)
#Branch = namedtuple('Branch', 'beg end offshoots')
# Tree = namedtuple('Tree', 'vtx trees')


SIZE = (1920+1080j)*0.6
WIDTH, HEIGHT = SIZE.real, SIZE.imag


class Tree:

	def __init__(self):
		self.vtx = 0+0j
		self.branches = []
		self.canvas = None
		self.IDs = []

	def coords(self, beg, end):
		return beg.real, beg.imag, end.real, end.imag

	def render(self, **options):
		for branch in self.branches:
			self.IDs.append(*self.coords(self.vtx, branch.vtx))
			branch.render(**options)

	def traverse(self):
		# TODO: Recursive traversal
		for branch in self.branch:
			yield branch



def tree(size, pos, angle, depth, ratio, offshoots):

	'''
	Generates a tree fractal, wherein each branch is represented
	as a pair of endpoint coordinates (or not, cf. TODO #2)

	size: of the first (and largest) 'branch'
 
	pos: position of the first branch
	angle: between two adjacent branches (radians; subject to change)
	ratio: between the size of a branch and that of its offshoots
	depth: recursive depth, ie. the number of levels
	offshoots: per (non-terminal) branch

	'''

	# TODO: Recursive or iterative solution (?)
	# TODO: Save data by using actual tree structure (?)
	# TODO: Independent coordinate system (cf. branchCoords) (?)
	# TODO: Generator
	# TODO: Recursive version
	# TODO: Make size a scalar (?)

	#def bifurcation(branch):
	def bifurcation(length, pos, rot, depth):
		return [Branch(pos, pos+length*rect(1, rot+n*angle), depth) for n in range(offshoots)]

	#trunk 	 = Branch(pos, pos+size*rect(1, RAD(-90)))
	# branches = bifurcation(size.real, pos, -90)
	branches = [Branch(pos, pos+size, 0)] #*rect(1, RAD(-90)))]

	#size *= ratio
	span  = angle*(offshoots-1) # Angle between the leftmost and rightmost offshoot TODO: Allow for varying angles
	start = -span/2 			# Angle of the leftmost offshoot (with respect to its parent branch)
	-RAD(15)

	#beg = trunk.end # First endpoint

	#level = 2 # Current level or depth (indexing 0 or 1?)
	#while True:
		#yield branches
	
	for level in range(1, depth):
		subtrees = []
		for subtree in range(offshoots**(level-1)):
			beg, end, depth, = branches[-offshoots**(level-1):][subtree]
			dθ = polar(end - beg)[1] # Angle offset of previous branch
			#angleOffset = asin((delta.imag)/sqrt((delta.real)**2 + (delta.imag)**2))*180.0/π
			subtrees += bifurcation(abs(size)*ratio**level, end, dθ+start, level)
		branches += subtrees
	
	return branches


def branchCoords(branch):
	return (int(branch.beg.real), int(branch.beg.imag), int(branch.end.real), int(branch.end.imag))


def renderTree(canvas, tree, **options):
	return [canvas.create_line(*branchCoords(branch), width=(5-branch.depth)*3, **options) for branch in tree]


def createContext(size):
	''' Initializes Window and Canvas '''
	window = tk.Tk()
	window.resizable(width=False, height=False)
	window.title('Fractals')
	# window.attributes('-alpha', 0.1)

	canvas = tk.Canvas(width=size.real, height=size.imag)
	canvas.pack()

	return Context(window, canvas)


def erase(branches, context):
	for b in branches:
		context.canvas.delete(b)

	
def animate(angle, context):
	#branches = tree(70-70j, SIZE*0.5, angle, 6, 0.70, 3)
	# TODO: Simulate swaying in the wind
	# TODO: Audio, loudness determines strength
	# TODO: Forest, leaves, snow
	# TODO: Accept arguments for tree properties
	branches = tree(rect(70, angle*5), SIZE*0.5, angle, 6, 0.70, 3)
	angle = angle % 360
	return renderTree(context.canvas, branches, capstyle=tk.ROUND, fill='#804040'), branches # '#%.2x%.2x%.2x' % (angle*3.2%255, angle%255, angle%255)), branches


def createAnimator(start, delta, context, fps):
	frames = (animate(angle, context) for angle in count(start, delta))
	prev, branches = [], []
	num = 0

	def forward():
		return next(frames)
	
	def nextFrame():
		nonlocal prev, branches, num
		erase(prev, context)
		prev, branches = forward()
		context.window.after(1000//fps, nextFrame)
		num += 1

	return nextFrame


def createProgressbar(pos, size, context, fps):
	return 0


keys = {
	'Left': False,
	'Right': False
}


def onKeyDown(event):
	keys[event.keysym] = True

def onKeyUp(event):
	keys[event.keysym] = False

	
	
def main():
	context = createContext(SIZE)
	sky 	= context.canvas.create_rectangle((0,0,WIDTH,HEIGHT//2), fill='#B8F3FA', width=0)
	ground 	= context.canvas.create_rectangle((0,HEIGHT//2,WIDTH,HEIGHT), fill='#07E40D', width=0)
	
	context.window.bind('<Key>', onKeyDown)
	context.window.bind('<KeyRelease>', onKeyUp)

	theta = RAD(45.0)
	dθ = RAD(2)

	branches = tree(rect(70, RAD(-90)), SIZE*0.5, theta, 5, 0.70, 3)
	IDs = renderTree(context.canvas, branches, fill='#633A03')

	def nudge():
		nonlocal theta, branches, IDs
		context.window.after(1000//30, nudge)
		if keys['Left']:
			theta -= dθ
		elif keys['Right']:
			theta += dθ
		else:
			return

		#erase(IDs, context) # TODO: Redraw and animate existing tree
		branches = tree(rect(70, RAD(-90)), SIZE*0.5, theta, 5, 0.70, 3)
		#IDs = renderTree(context.canvas, branches, fill='#633A03')
		for twig, ID in zip(branches, IDs):
			context.canvas.coords(ID, *branchCoords(twig))

	nudge()
	#createAnimator(RAD(0), RAD(0.8), context, 30)()
	

	context.window.mainloop()


if __name__ == '__main__':
	main()
