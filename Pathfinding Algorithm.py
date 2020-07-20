#!/usr/bin/python3 

# importing modules  
import pygame
import math
from queue import PriorityQueue

WIDTH = 800 # width of the screen 
WIN = pygame.display.set_mode((WIDTH, WIDTH)) # setting the display boundaries 
pygame.display.set_caption("A* Path Finding Algorithm") # pygame window caption 

# ---- RGB VALUES SET ----  
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row # row in a grid 
		self.col = col # collumn in a grid 
		self.x = row * width # x boundary 
		self.y = col * width # y boundary 
		self.color = WHITE # main color 
		self.neighbors = [] # node neighbor 
		self.width = width # width of the node 
		self.total_rows = total_rows # total number of rows in a grid 

	def get_pos(self): 
		return self.row, self.col

	def is_closed(self): # closed node is represented by red 
		return self.color == RED

	def is_open(self): # open node is represented by green 
		return self.color == GREEN

	def is_barrier(self): # barrier node is represented by black 
		return self.color == BLACK

	def is_start(self): # start node is represented by orange 
		return self.color == ORANGE

	def is_end(self): # end node is represented by turqoise 
		return self.color == TURQUOISE

	def reset(self): # reseting the color 
		self.color = WHITE

	def make_start(self): 
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color  = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width)) # drawing a node 

	def update_neighbors(self, grid):
		self.neighbors = [] # list of neighbors 
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # moving down a row 
			self.neighbors.append(grid[self.row + 1][self.col]) # appending the next row down 

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # moving up a row 
			self.neighbors.append(grid[self.row - 1][self.col]) # appending the next row up 

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # moving right a row 
			self.neighbors.append(grid[self.row][self.col + 1]) # appending the next row right 

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # moving left a row 
			self.neighbors.append(grid[self.row][self.col - 1]) # appending the next row left 

	def __lt__(self, other):
		return False


def heuristic_function(point1, point2): # heuristic function calculating the distances 
	# ---- setting points 1 and 2 ---- 
	x1, y1 = point1 
	x2, y2 = point2

	return abs(x1 - x2) + abs(y1 - y2) # heuristic function calculation 

def algorithm(draw, grid, start, end): 
	count = 0
	open_set = PriorityQueue() # making a open set for the nodes  
	open_set.put((0, count, start)) # putting a f.score value to the open set that starts with 0 
	came_from = {} # where did the node came from? 
	g_score = {node: float("inf") for row in grid for node in row} # making a dictionary for g.score, starting at infinity(inf)
	g_score[start] = 0 # setting the g.score of start 
	f_score = {node: float("inf") for row in grid for node in row} # making a dictionary for f.score, starting at infinity(inf) 
	f_score[start] = heuristic_function(start.get_pos(), end.get_pos()) # setting the f.score with the heuristic function 
	
	open_set_hash = {start} # making a hash but with a different data structure 

	while not open_set.empty(): 
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: # if the user tries to exits the program 
				pygame.quit() # pygame program quits 

		current = open_set.get()[2] # getting the current node we are looking at 
		open_set_hash.remove(current) # removing the current node so we don't end up with duplicates 

		# if we found the end node 
		if current == end:
			reconstruct_path(came_from, end, draw) # making the path 
			end.make_end() 
			return True

		for neighbor in current.neighbors: 
			temp_g_score = g_score[current] + 1 # setting a temporary g.score value + 1 

			# updating the values for a better path 
			if temp_g_score < g_score[neighbor]: 
				came_from[neighbor] = current 
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + heuristic_function(neighbor.get_pos(), end.get_pos())

				# checking if the neighbor in the open set hash 
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor)) # putting a new neighbor, because it has a better path 
					open_set_hash.add(neighbor)  
					neighbor.make_open() # making the neighbor node open 
		draw()
		if current != start:
			current.make_closed() # making a closed node 
	return False

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def make_grid(rows, width): # function for grid 
	grid = [] # grid array 
	gap = width // rows # checking width of the nodes 
	for i in range(rows):
		grid.append([]) 
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node) # appending a node to the grid list 
	return grid # returning the grid 

def draw_grid(win, rows, width): # function for drawing the grid 
	gap = width // rows # checking the width of then nodes 
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # drawing a horizontal line 
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) # drawing a vertical line 

def draw(win, grid, rows, width):
	win.fill(WHITE) # filling the background with white 
	for row in grid:
		for node in row:
			node.draw(win) # drawing a node 

	draw_grid(win, rows, width) # drawing a grid 
	pygame.display.update() # updating the display 


def get_clicked_pos(pos, rows, width):
	gap = width // rows # checking the node width 
	y, x = pos # y and x position 
	row = y // gap
	col = x // gap
	return row, col

def main(win, width):
	ROWS = 20 # number of rows 
	grid = make_grid(ROWS, width) # making a grid 

	start = None 
	end = None 

	run = True # did the program start 

	while run: # while the program is running 
		draw(win, grid, ROWS, width) # drawing the grid and nodes 
		# checking all the events during the program 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False 

			if pygame.mouse.get_pressed()[0]: # left mouse button press 
				pos = pygame.mouse.get_pos() 
				row, col = get_clicked_pos(pos, ROWS, width)  # getting the mouse click position
				node = grid[row][col]
				if not start and node != end:
					start = node # start node 
					start.make_start() # making a start node 

				elif not end and node != start:
					end = node # end node 
					end.make_end() # making an end node 

				elif node != end and node != start:
					node.make_barrier() # making a barrier 

			elif pygame.mouse.get_pressed()[2]: # right mouse button press 
				pos = pygame.mouse.get_pos()  
				row, col = get_clicked_pos(pos, ROWS, width) # getting the mouse click position
				node = grid[row][col]
				node.reset() # reseting nodes 
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN: # if the key is pressed 
				if event.key == pygame.K_SPACE and  start and  end: # if the user the space key the algorithms starts 
					for row in grid: 
						for node in row: 
							node.update_neighbors(grid) # updating all neighbours 

					# lambda - anonymous function 
					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) # calling the algorithm and starting it 
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit() # quiting the program 
if __name__ == '__main__': 
	main(WIN, WIDTH)  