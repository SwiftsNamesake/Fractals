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
from collections import namedtuple
from itertools import count
from random import random
from math import sqrt, asin
from cmath import sin, cos, rect, polar, pi as π


Context = namedtuple('Context', 'window, canvas')
Branch  = namedtuple('Branch', 'beg end depth')
# TODO: Include angle in Branch (?)
#Branch = namedtuple('Branch', 'beg end offshoots')
# Tree = namedtuple('Tree', 'vtx trees')


SIZE = (1920+1080j)*0.6
WIDTH, HEIGHT = SIZE.real, SIZE.imag


def RAD(deg):
	return deg*π/180.0


def DEG(rad):
	return rad*180.0/π


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

	#beg = trunk.end # First endpoint

	#level = 2 # Current level or depth (indexing 0 or 1?)

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
	return [canvas.create_line(*branchCoords(branch), **options) for branch in tree]


def createContext(size):
	''' Initializes Window and Canvas '''
	window = tk.Tk()
	window.resizable(width=False, height=False)
	window.title('Fractals')

	canvas = tk.Canvas(width=size.real, height=size.imag)
	canvas.pack()

	return Context(window, canvas)


def erase(branches, context):
	for b in branches:
		context.canvas.delete(b)

	
def animate(angle, context):
	#branches = tree(70-70j, SIZE*0.5, angle, 6, 0.70, 3)
	branches = tree(rect(70, angle*2), SIZE*0.5, angle, 6, 0.70, 3)
	angle = angle % 360
	return renderTree(context.canvas, branches, width=4, fill='#804040'), branches # '#%.2x%.2x%.2x' % (angle*3.2%255, angle%255, angle%255)), branches


def createAnimator(start, delta, context, fps):
	frames = (animate(angle, context) for angle in count(start, delta))
	prev, branches = [], []

	def forward():
		return next(frames)
	
	def nextFrame():
		nonlocal prev, branches
		erase(prev, context)
		prev, branches = forward()
		#print(*((x-DEG(delta/2), x+DEG(delta/2)) for x in (0, 90, 180, 270)))
		#straight = any(mini <= DEG(polar(branches[-1].end-branches[-1].beg)[1]) <= maxi for mini, maxi in ((x-DEG(delta/2), x+DEG(delta/2)) for x in (0, 90, 180, 270)))
		#print(straight)
		context.window.after(1000*3 if False else 1000//fps, nextFrame)

	return nextFrame


def createProgressbar(pos, size, context, fps):
	return 0


def main():
	context = createContext(SIZE)
	#branches = tree(50+0j, 1920/3/2+1080j/3-70j, 20, 4, 0.60, 3)
	#prev = renderTree(context.canvas, branches, width=3)
	createAnimator(RAD(0), RAD(0.8), context, 30)()

	context.window.mainloop()


if __name__ == '__main__':
	main()