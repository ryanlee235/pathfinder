import random
import pygame 
from queue import PriorityQueue

WIDTH = 600

SURFACE = pygame.display.set_mode((WIDTH, WIDTH))

#node colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)
MAROON = (128, 0, 0)
GRAY = (128, 128, 128)

class Node:
    def __init__(self, rows, column, width, total_rows):
        self.rows = rows
        self.column = column
        self.width = width
        self.total_rows = total_rows
        self.x = rows * width 
        self.y = column * width
        self.color = WHITE
        self.neighbors = []
    def start(self):
        return self.color == DARK_GREEN

    def end(self):
        return self.color == MAROON

    def barrier(self):
        return self.color == BLACK

    def path(self):
        return self.color == BLUE

    def open(self):
        return self.color == GREEN

    def closed(self):
        return self.color == RED

    def make_start(self):
        self.color = DARK_GREEN
    
    def make_end(self):
        self.color = MAROON
    
    def make_barrier(self):
        self.color = BLACK

    def make_path(self):
        self.color = BLUE

    def make_open(self):
        self.color = GREEN
    
    def make_closed(self):
        self.color = RED

    def make_reset(self):
        self.color = WHITE

    def get_pos(self):
        return self.rows, self.column
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))

    def neighbor(self, grid):
        self.neighbors = []
        #if the rows dont go passed the specified width and height
        #well add the row to the list below the node
        if self.rows < self.total_rows -1 and not grid[self.rows + 1][self.column].barrier():#down
            self.neighbors.append(grid[self.rows + 1][self.column])           
        # if the rows is not at the start of the window
        #add the node above the current node
        if self.rows > 0 and not grid[self.rows -1][self.column].barrier():#up
            self.neighbors.append(grid[self.rows -1][self.column])
        # if the column doesnt go passed the window
        # add the node to the right
        if self.column < self.total_rows -1 and not grid[self.rows][self.column + 1].barrier():#right
            self.neighbors.append(grid[self.rows][self.column +1])
        # if the column is not the start
        #add the node to the left
        if self.column > 0 and not grid[self.rows][self.column - 1].barrier():#left
            self.neighbors.append(grid[self.rows][self.column -1])
    
    def __lt__(self, other):
        return False
#calculating our mannhattan distance
def h(position1, position2):
    x1, y1 = position1
    x2, y2 = position2
    return abs(x1 - x2) + abs(y1 - y2)

def path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
	count = 0
	# our set of nodes that will be next
	open_set = PriorityQueue()
	#starting stuff to put into the queue
	open_set.put((0, count, start))
	#this will store all of the nodes that it tooks for us to get to the end node
	came_from = {}
	# g score is going to contain our spot and a float this is infinty
	g_score = {spot: float("inf") for row in grid for spot in row}
	# our g score will always start at 0
	g_score[start] = 0

	f_score = {spot: float("inf") for row in grid for spot in row}
	# 
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}


	#while the alogrithm is running, you can still quit if there is an issue
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		#grabbing our start node
		current = open_set.get()[2]
		#removing it from our open_set, becasue it was looked at 
		open_set_hash.remove(current)
		#if we found the end node, we'll reconstruct a path 
		if current == end:
			path(came_from, end, draw)
			end.make_end()
			return True
		#accessing the neighbors list for our node class
		for neighbor in current.neighbors:
			#adding 1 to our g score to look at neigbors 
			temp_g_score = g_score[current] + 1
			# the current g score is less than the g score of the neigbor
			if temp_g_score < g_score[neighbor]:
				# making the neighbor our current node to look at
				came_from[neighbor] = current
				# take the g_score and add it to our new node
				g_score[neighbor] = temp_g_score
				# adding the g score and the h score to the f score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				#putting the next node into the open set
				if neighbor not in open_set_hash:
					count += 1
					#put our f score in, our next node
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def make_grid(rows, width):
    #empty list to store our node for later
    grid = []
    #getting the size of the cubes in our grid
    cube_size = width // rows

    #for the size of the rows, were adding an empty list in
    for x in range(rows):
        grid.append([])
        for y in range(rows):
            node = Node(x, y, cube_size, rows)
            #appending our node to the empyt list that was created for x
            grid[x].append(node)
    return grid

def draw_grid(surface, rows, width):
    cube_size = width // rows

    for x in range(rows):
        #drawing our x coordinates lines
        pygame.draw.line(surface, GRAY, (0, x * cube_size), (width, x * cube_size))
        for y in range(rows):
            #draws our lines for our y coordinates lines
            pygame.draw.line(surface, GRAY, (y * cube_size, 0), (y * cube_size, width))

def draw(surface, grid, rows, width):
    surface.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(surface)
    draw_grid(surface, rows, width)
    pygame.display.update()



def mouse_pos(position, rows, width):
    cube_size = width // rows
    y, x = position

    row = y // cube_size
    column = x // cube_size

    return row, column

def random_barrier(rows, grid,start, end):
    count = 0 
    x = random.randrange(0, rows, 1)
    y = random.randrange(0, rows, 1)
    node = grid[x][y]
    if start != end and node != start:
        node.make_barrier()
    

def main(win, width):
	ROWS = 40
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = mouse_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					random_barrier(ROWS, grid, start, end)

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = mouse_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.make_reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.neighbor(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()     
            

main(SURFACE, WIDTH)
