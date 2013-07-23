import random
import sys
import pygame
from pygame.locals import *


w,h = (20,20)
width,height = (w*32,h*32)

def init_grid():
	grid = []
	for i in range(h):
		grid.append([])
		for j in range(w):
			grid[i].append(0)
	return grid

bombs = init_grid()
grid = init_grid()
flags = init_grid()
revealed = init_grid()


def make_grid():
	for i in range(h):
		for j in range(w):
			if random.random() > 0.85:
				bombs[i][j] = 1
				
				if i > 0:
					if j > 0:
						grid[i-1][j-1]	+= 1
					if j < w-1:
						grid[i-1][j+1] 	+= 1
					grid[i-1][j] 	+= 1

				if j > 0:
					grid[i][j-1]	+= 1
				if j < w-1:
					grid[i][j+1]	+= 1

				if i < h-1:
					grid[i+1][j]	+= 1
					if j > 0:
						grid[i+1][j-1]	+= 1
					if j < w-1:
						grid[i+1][j+1]	+= 1
	return grid, bombs

	
def print_grid(show_bombs=False):
	for i in range(h):
		s = ""
		for j in range(w):
			if show_bombs and bombs[i][j]:
				s += "x "
			elif flags[i][j]:
				s += "F "
			elif revealed[i][j]:
				if bombs[i][j]:
					s += "x "
				else:
					s += str(grid[i][j])+" "
			else:
				s += ". "
		print s


def draw_grid(bgd):
	spacing = int(width/w)
	for j in range(1,h):
		pygame.draw.line(bgd, (100,100,100), (j*spacing,1), (j*spacing,width))
	for i in range(1,w):
		pygame.draw.line(bgd, (100,100,100), (1,i*spacing), (height,i*spacing))


def propagate_zero(y,x):
	print "prop: ",y,x
	if grid[y][x] == 0:
		revealed[y][x] = 1
		
		for stepy in [-1,1]:
			for stepx in [-1,1]:
				yy = y+stepy
				xx = x+stepx
				if grid[yy][xx] == 0 and bombs[yy][xx] == 1:
					propagate_zero(yy,xx)
				else:
					revealed[yy][xx] = 1


def init_screen():
	window = pygame.display.set_mode((width,height))
	pygame.display.set_caption("Minesweeper")
	return pygame.display.get_surface()


def play():
	pygame.init()
	screen = init_screen()
	make_grid()
	clock = pygame.time.Clock()
	draw_grid(screen)

	while True:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				mousex, mousey = event.pos
				y = int(h * mousey / height)
				x = int(w * mousex / width)
				revealed[y][x] = 1
				if event.button == 1:
					flags[y][x] = 0
					if bombs[y][x]:
						print "GAME OVER"
						# sys.exit(0)
				elif event.button == 3:
					flags[y][x] = 1

			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit(0)
					pygame.event.post(pygame.event.Event(QUIT))

		pygame.display.flip()
		clock.tick()


play()
