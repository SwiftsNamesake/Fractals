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
from math import sin, cos, pi as π
from math import sqrt, asin, sin, cos
from cmath import rect, polar, pi as π # sin, cos, 
from random import randint
from functools import reduce

from SwiftUtils import Console

code = [
	'<fg=DEF>def</> <fg=FUN>RAD</>(<fg=ARG>deg</>):',
	'    <fg=OP>return</> <fg=VAR>deg</><fg=OP>*</><fg=VAR>pi</><fg=OP>/</><fg=LIT>180.0</>',
	'',
	'<fg=OP>while</> <fg=LIT>True</>:',
	'    <fg=DEF>print</>(<fg=STR>\'Corvus corax Felix Phalanx\'</>)',
	'    <fg=DEF>print</>(<fg=STR>\'Venison\'s deer, isn\'t it?\'</>)',
	'    <fg=DEF>print</>(<fg=STR>\'</><fg=LIT>\\\'</><fg=STR>Tis a consummation...\'</>)'
]#[2:]

# Background: #272822
# Def: # 102 217 239
# Arg: # 253 151 32
# Operator: # 249 39 114
# Literal: # 141 129 255
# String: # 230 219 116
# Variable: # 248 248 242

colours = {
	'BG': 	(39, 40, 34),		# Background
	'DEF': 	(102, 217, 239),	# Def keyword
	'ARG': 	(253, 151, 32),		# Argument
	'OP': 	(249, 39,  114),	# Operator
	'LIT': 	(141, 129, 255),	# Literal
	'STR': 	(230, 219, 116),	# String
	'VAR': 	(248, 248, 242),	# Variable
	'FUN': 	(166, 182, 36),		# Function name
	'WHITE': (255, 255, 255),	#
	'BLACK': (0, 0, 0)
	# 'COM': () # Comment
}


def renderLine(line, size, font, pos):
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
	return reduce(lambda prev, token: prev+[(renderToken(token), totalSize(prev))], line, [])

	#return [(pygame.font.SysFont(font, size).render(token.text, 2, colours[token.fg]),
	#		(pos[0]+size*0.62*sum(len(prev.text) for prev in line[:n]), pos[1])) for n, token in enumerate(line)]
	# TODO: Offset for each token (?)


def renderLines(lines, size, font, pos):
	raise NotImplementedError


def mergeSurfaces(surfaces):
	raise NotImplementedError


def RAD(deg):
	return deg*π/180.0


def DEG(rad):
	return rad*180.0/π


def star(surface, pos, length, points, colour, theta=0):
	vertices = [(pos[0]+length*cos(p*2*π/points-theta), pos[1]+length*sin(p*2*π/points-theta)) for p in range(points)]
	return pygame.draw.aalines(surface, colour, True, vertices[::2]+vertices[1::2], 2)


def createContext(size):
	pygame.init()
	surface = pygame.display.set_mode(size)
	clock = pygame.time.Clock()
	return surface, clock


def main():
	surface, clock = createContext((1024, 1024//2))

	θ = 0.0

	#print('\n'.join(pygame.font.get_fonts()))

	#labels = [(pygame.font.SysFont(font, 20).render(font, 3, (0x34, 0xDF, 0x3D)), pygame.font.SysFont(font, 20).render(font, 3, (0,0,0))) for font in pygame.font.get_fonts()[:50]]
	labels = [pygame.font.SysFont(font, 20).render(font, 3, (randint(0, 255), randint(0, 255), randint(0, 255))) for font in pygame.font.get_fonts()[:100]]

	# Syntax highlighting
	con = Console.Console()
	# TODO: Lambda serveing the purpose of a let expression (?)
	lines = (lambda size: [renderLine(con.parseMarkup(line), size, ['kristenitc', 'oldenglishtext', 'emilbus mon'][0], (400, 20+n*size)) for n, line in enumerate(code)])(22)

	# Images
	dice = pygame.image.load('C:/Users/Jonatan/Desktop/Python/resources/dice.png').convert()

	while True:
		ev = pygame.event.poll()
		if ev.type == pygame.QUIT:
			break;
		elif ev.type == pygame.MOUSEMOTION:
			pass

		surface.fill([(0, 72, 50), (0xFF, 0xFF, 0), colours['BG']][2])
		θ += 0.02

		pygame.draw.polygon(surface, ((255+255*cos(θ))//2, (255+255*sin(θ))//2, 0xF9), (lambda sides: [(160+60*(sin(θ)+1.5)*cos(θ+s*2*π/sides),
																		  160+60*(sin(θ)+1.5)*sin(θ+s*2*π/sides)) for s in range(sides)])(10), 5)
		pygame.draw.circle(surface, (0xFF, 0x2C, 0x1C), (650, 425), 60, 5)
		# pygame.gfxdraw.aacircle(surface, (0xFF, 0x2C, 0x1C), (650, 425), 60, 5)
		pygame.draw.aaline(surface, (0x84, 0x9B, 0xF9), (650+60*cos(θ*0.5), 425+60*sin(θ*0.5)), (650+60*cos(θ*0.2), 425+60*sin(θ*0.2)), 5)
		star(surface, (200, 200), 45, 7, (0xCE, 0x26, 0x1E), π/2+θ)
		
		surface.blit(dice, (200, 200))

		for n, line in enumerate(lines):
			for token in line:
				surface.blit(token[0], (token[1][0], token[1][1]+n*15))

		for n, label in enumerate(labels):
			# surface.blit(label[1], (52, 52+n*25-(θ*30)%(25*len(labels))))
			# surface.blit(label[0], (50, 50+n*25-(θ*30)%(25*len(labels))))
			surface.blit(label, (50, 50+n*25-(θ*30)%(25*len(labels))))
			# surface.blit(pygame.transform.rotate(label, 12), (50, 50+n*25-(θ*30)%(25*len(labels))))
			#surface.blit(pygame.transform.laplacian(label[0]), (50, 50+n*25-(θ*30)%(25*len(labels))))

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()

if __name__ == '__main__':
	main()