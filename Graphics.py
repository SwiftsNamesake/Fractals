#
# Fractals - Graphics
#
# Jonatan H Sundqvist
# August 23 2014
#


# TODO | - List of frame generators (?)
#		 - 3D, bezier curves, fonts, etc

# SPEC | - 
#		 - 


import pygame
from math import sin, cos, sqrt, asin, copysign, pi as π
from cmath import rect, polar, pi as π # sin, cos, 
from random import randint
from functools import reduce

from SwiftUtils import Console
from Utilities import *

import Fractals


code = [
	'<fg=DEF>class</> Nihilo:',
	'    <fg=DEF>def</> <fg=DEF>__init__</>(<fg=ARG>self</>, <fg=ARG>ex</>):',
	'        <fg=VAR>self</>.ex <fg=OP>=</> <fg=VAR>ex</>',
	'        <fg=VAR>self</>.creatio <fg=OP>=</> <fg=VAR>creatio</>',
	'',
	'<fg=DEF>def</> <fg=FUN>RAD</>(<fg=ARG>deg</>):',
	'    <fg=OP>return</> <fg=VAR>deg</><fg=OP>*</><fg=VAR>pi</><fg=OP>/</><fg=LIT>180.0</>',
	'',
	'<fg=OP>while</> <fg=LIT>True</>:',
	'    <fg=DEF>print</>(<fg=STR>\'Corvus corax Felix Phalanx\'</>)',
	'    <fg=DEF>print</>(<fg=STR>\'Venison\'s deer, isn\'t it?\'</>)',
	'    <fg=DEF>print</>(<fg=STR>\'</><fg=LIT>\\\'</><fg=STR>Tis a consummation...\'</>)',
	'',
	'<fg=OP>for</> <fg=VAR>letter</> <fg=OP>in</> <fg=STR>\'Jonatan\'</>:',
	'    <fg=COM># Prints each letter in my name</>',
	'    <fg=DEF>print</>(<fg=STR>\'There is a</> <fg=LIT>%s</> <fg=STR>in my name.\'</> <fg=OP>%</> <fg=VAR>letter</>)',
	#'    <fg=DEF>print</>(<fg=STR>\'There is a</> <fg=LIT>%s</> <fg=STR>in my name.\'</>.<fg=DEF>format</>(<fg=VAR>letter</>))'
	'',
	'<fg=OP>if</> <fg=VAR>__name__</> <fg=OP>==</> <fg=STR>\'__main__\'</>:',
	'    <fg=VAR>main</>()'
]#[2:]

# Background: #272822
# Def: # 102 217 239
# Arg: # 253 151 32
# Operator: # 249 39 114
# Literal: # 141 129 255
# String: # 230 219 116
# Variable: # 248 248 242

# TODO: More properties (eg. fonts, italics), nesting
colours = {
	'BG': 	(39, 40, 34),		# Background
	'DEF': 	(102, 217, 239),	# Def keyword
	'ARG': 	(253, 151, 32),		# Argument
	'OP': 	(249, 39,  114),	# Operator
	'LIT': 	(141, 129, 255),	# Literal
	'STR': 	(230, 219, 116),	# String
	'VAR': 	(248, 248, 242),	# Variable
	'FUN': 	(166, 182, 36),		# Function name
	'COM': 	(107, 113, 94),		# Comment
	'WHITE': (255, 255, 255),	#
	'BLACK': (0, 0, 0)			#
}



#==============================================================================
# Typography
#==============================================================================
def renderLine(line : '[Tokens]', size : int, font : str, pos : '(int, int)') -> '[Surface]':
	# TODO: Width of previous strings (currently assumed to be size)
	# TODO: Combine tokens in a single surface (?)
	# TODO: Save font object(?)
	# TODO: Text selection (cf. Font.metrics)
	#print(line)
	#reduce

	font = pygame.font.SysFont(font, size)

	def totalSize(tokens):
		return pos[0]+sum(token[0].get_size()[0] for token in tokens), pos[1]

	def renderToken(token):
		return font.render(token.text, 2, colours[token.fg])

	# Font.get_linesize
	return reduce(lambda prev, token: prev+[(renderToken(token), totalSize(prev))], line, []) # TODO: Cache the size calculations (?)

	#return [(pygame.font.SysFont(font, size).render(token.text, 2, colours[token.fg]),
	#		(pos[0]+size*0.62*sum(len(prev.text) for prev in line[:n]), pos[1])) for n, token in enumerate(line)]
	# TODO: Offset for each token (?)


def renderLines(lines, size, font, pos):
	# TODO: Vertical padding, different fonts and line heights
	# TODO: Merge buffers (?)
	def nextItem(prev, tokens):
		line = renderLine(tokens, size, font, (pos[0], prev[0]))
		# print(line)
		return (prev[0]+line[0][0].get_size()[1], prev[1]+[line])

	return reduce(lambda prev, line: nextItem(prev, line), lines, (pos[1], []))[1]
	raise NotImplementedError


def mergeSurfaces(surfaces):
	raise NotImplementedError


#==============================================================================
# Graphics
#==============================================================================
def star(surface, pos, length, points, colour, theta=0):
	vertices = [(pos[0]+length*cos(p*2*π/points-theta), pos[1]+length*sin(p*2*π/points-theta)) for p in range(points)]
	return pygame.draw.aalines(surface, colour, True, vertices[::2]+vertices[1::2], 2)


def renderTree(surface, tree, colour):
	return [pygame.draw.aaline(surface, colour, (branch.beg.real, branch.beg.imag), (branch.end.real, branch.end.imag)) for branch in tree]


#==============================================================================
# Windows and events
#==============================================================================
def createContext(size):
	pygame.init()
	surface = pygame.display.set_mode(size)
	clock = pygame.time.Clock()
	return surface, clock


def main():
	SIZE = (int(1024*2*0.75), 720)
	surface, clock = createContext(SIZE)

	θ = 0.0

	# TODO: Click and drag
	# TODO: Scroll inertia (...)
	scrollX, scrollY = 0.0, 0.0
	dxScroll, dyScroll = 0.0, 0.0
	intensity = 1.25 # Intensity of scroll bar

	# Typography
	fontNames = ['kristenitc', 'oldenglishtext', 'emilbus mon', 'blackletter']

	labels = [pygame.font.SysFont(font, 20).render(font, 3, (randint(0, 255), randint(0, 255), randint(0, 255))) for font in pygame.font.get_fonts()[:100]]

	# TODO: Lambda serveing the purpose of a let expression (?)
	con = Console.Console()
	#lines = (lambda size: [renderLine(con.parseMarkup(line), size, ['kristenitc', 'oldenglishtext', 'emilbus mon'][0], (400, 20+n*size)) for n, line in enumerate(code)])(22)

	# Images
	dice = pygame.image.load('C:/Users/Jonatan/Desktop/Python/resources/dice.png').convert()

	# Mouse
	# TODO: Dynamic text utilities
	mouse = pygame.mouse.get_pos()
	mFont = pygame.font.SysFont('oldenglishtext', 20)
	mMarkup = renderLines([con.parseMarkup('<fg=OP>X</>: %d' % mouse[0]), con.parseMarkup('<fg=OP>Y</>: %d' % mouse[1])], 20, 'oldenglishtext', (20, 20))
	# print(mMarkup)
	mCoords = None
	mPrev = None

	# Main loop
	while True:
		ev = pygame.event.poll()
		if ev.type == pygame.QUIT:
			break;
		elif ev.type == pygame.MOUSEMOTION:
			mouse = ev.pos
			#mCoords = mFont.render('X: %d | Y: %d' % mouse, 3, (0xFC, 0xCC, 0x3E))
			coll = pygame.Rect(SIZE[0]-15, -scrollY, 10, 60).collidepoint(ev.pos)
			intensity = 1.5 if coll else 1.25
			if coll and pygame.mouse.get_pressed()[0]:
				scrollY = -(mouse[1]-mPrev[1])
				mPrev = mouse
		elif (ev.type == pygame.MOUSEBUTTONDOWN) and (ev.button in (4, 5)):
			# Scroll
			#dxScroll += (1 if ev.button == 4 else -1)*7
			dyScroll += (1 if ev.button == 4 else -1)*7
			print('scroll')
		elif (ev.type == pygame.MOUSEBUTTONDOWN) and (ev.button == 1):
			mPrev = pygame.mouse.get_pos()
		
		# Scroll
		scrollX += dxScroll
		scrollY += dyScroll
		dxScroll += sign(-dxScroll)*0.25
		dyScroll += sign(-dyScroll)*0.25

		# Background
		surface.fill([(0, 72, 50), (0xFF, 0xFF, 0), colours['BG']][2])
		θ += 0.02

		# Mouse
		if mCoords is not None:
			#surface.blit(mCoords, (20, 20))
			for token, pos in mMarkup:
				surface.blit(token, pos)
		#pygame.draw.polygon(surface, ((255+255*cos(θ))//2, (255+255*sin(θ))//2, 0xF9), (lambda sides: [(160+60*(sin(θ)+1.5)*cos(θ+s*2*π/sides),
		#																  160+60*(sin(θ)+1.5)*sin(θ+s*2*π/sides)) for s in range(sides)])(10), 5)

		pygame.draw.aalines(surface, ((255+255*cos(θ))//2, (255+255*sin(θ))//2, 0xF9), True, (lambda sides: [(160+60*(sin(θ)+1.5)*cos(θ+s*2*π/sides),
																		  160+60*(sin(θ)+1.5)*sin(θ+s*2*π/sides)) for s in range(sides)])(10), 5)
		
		X, Y = 830, 80
		pygame.draw.circle(surface, (0xFF, 0x2C, 0x1C), (X, Y), 60, 5)
		# pygame.gfxdraw.aacircle(surface, (0xFF, 0x2C, 0x1C), (650, 425), 60, 5)
		pygame.draw.aaline(surface, (0x84, 0x9B, 0xF9), (X+60*cos(θ*0.5), Y+60*sin(θ*0.5)), (X+60*cos(θ*0.2), Y+60*sin(θ*0.2)), 5)
		star(surface, (200, 200), 45, 7, (0xCE, 0x26, 0x1E), π/2+θ)
		
		#pygame.transform.rotate(dice, θ*15)
		surface.blit(dice, (200, 200))

		# Scrollbar
		# TODO: Glow on hover
		pygame.draw.rect(surface, (colours['BG'][0]*intensity, colours['BG'][0]*intensity, colours['BG'][0]*intensity), pygame.Rect(SIZE[0]-15, -scrollY, 10, 60))

		# Blit code
		for n, line in renderLines(code, 20, fontNames[0], (300, 40)):
			for token, pos in line:
				surface.blit(token, pos)
			
		# Blit coords
		for n, line in enumerate(renderLines([con.parseMarkup('<fg=OP>X</>: <fg=LIT>%d</>' % mouse[0]),
											  con.parseMarkup('<fg=OP>Y</>: <fg=LIT>%d</>' % mouse[1])], 20, 'oldenglishtext', (20, 20))):
			for token, pos in line:
				surface.blit(token, pos)

		# Blit font names
		for n, label in enumerate(labels):
			# surface.blit(label[1], (52, 52+n*25-(θ*30)%(25*len(labels))))
			# surface.blit(label[0], (50, 50+n*25-(θ*30)%(25*len(labels))))
			surface.blit(label, (50, 50+n*25-(θ*30)%(25*len(labels))))
			# surface.blit(pygame.transform.rotate(label, 12), (50, 50+n*25-(θ*30)%(25*len(labels))))
			#surface.blit(pygame.transform.laplacian(label[0]), (50, 50+n*25-(θ*30)%(25*len(labels))))

		renderTree(surface, Fractals.tree(rect(70, θ), (SIZE[0]*0.5+SIZE[1]*0.5j), θ*0.5, 6, 0.70, 3), (0xCF, 0xCC, 0x15))
		pygame.display.flip()
		clock.tick(60)

	pygame.quit()

if __name__ == '__main__':
	main()