import random
import sys

w,h = (20,20)

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


def play():
	make_grid()
	print_grid()

	finished = False
	while not finished:
		s = raw_input()
		c = s.split(",")
		y = int(c[0]) - 1
		x = int(c[1]) - 1

		revealed[y][x] = 1
		# propagate_zero(y,x)

		flag = False
		if len(c) > 2:
			flag = c[2] == "F"
		if flag:
			flags[y][x] = 1
		else:
			flags[y][x] = 0

		if not flag and bombs[y][x]:
			print ""
			print "GAME OVER"
			print_grid(True)
			sys.exit(0)
		print_grid()

play()
