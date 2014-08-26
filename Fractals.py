#
# Fractals - Fractals
#
# Jonatan H Sundqvist
# August 26 2014
#


# TODO | - 
#		 - 

# SPEC | - 
#		 - 


from math import sin, cos, sqrt, asin, copysign, pi as π
from cmath import rect, polar, pi as π # sin, cos, 
from collections import namedtuple
from Utilities import *


# Context = namedtuple('Context', 'window, canvas')
Branch  = namedtuple('Branch', 'beg end depth')
# TODO: Include angle in Branch (?)
#Branch = namedtuple('Branch', 'beg end offshoots')
# Tree = namedtuple('Tree', 'vtx trees')


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

