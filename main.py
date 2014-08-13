#
# Fractals.py
# Creating recursive geometries with tkinter
#
# Jonatan H Sundqvist
# August 13 2014
#

# TODO | -
#		 -

# SPEC | -
#		 -


import tkinter as tk
from collections import namedtuple


Context = namedtuple('Context', 'window, canvas')


def createContext():
	''' Initializes Window and Canvas '''
	window = tk.Tk()
	window.resizable(width=False, height=False)
	window.title('Fractals')

	canvas = tk.Canvas(width=1920//3, height=1080//3)
	canvas.pack()

	return Context(window, canvas)


def main():
	context = createContext()
	context.window.mainloop()
	

if __name__ == '__main__':
	main()