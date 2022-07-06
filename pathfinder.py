from ctypes import c_ubyte
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

    def position(self):
        return self.rows, self.column
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))

    def neighbor(self, grid):
        self.neighbors = []
        #if the rows dont go passed the specified width and height
        #well add the row to the list below the node
        if self.rows < self.total_rows -1 and not grid[self.rows + 1][self.column].make_barrier():#down
            self.neighbors.append(grid[self.rows + 1][self.column])           
        # if the rows is not at the start of the window
        #add the node above the current node
        if self.rows > 0 and not grid[self.rows -1][self.column].make_barrier():#up
            self.neighbors.append(grid[self.rows -1][self.column])
        # if the column doesnt go passed the window
        # add the node to the right
        if self.column < self.total_rows -1 and not grid[self.rows][self.column + 1].make_barrier():#right
            self.neighbors.append(grid[self.rows][self.column +1])
        # if the column is not the start
        #add the node to the left
        if self.column > 0 and not grid[self.rows][self.column - 1].make_barrier():#left
            self.neighbors.append(grid[self.rows][self.column -1])

#calculating our mannhattan distance
def h(position1, position2):
    x1, x2 = position1
    y1, y2 = position2
    return abs(x1 - x2) + abs(y1 - y2)

def path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def astar(draw, grid, start, end):
    count = 0
    #will allow us to check the next node that is entered in
    open_set = PriorityQueue
    #putting our start node in to the list first
    open_set.put((0, count, start))
    came_from = {}
    #setting a dictionary that will contain all of the nodes
    g_score = {}
    f_score = {}
    # will allow us to keep track of what will be in the open_set.
    open_set_hash = {start}

    for row in grid:
        for node in row:
            g_score[node] = float('inf')
            f_score[node] = float('inf')

    g_score[start] = 0
    f_score[start] = h(start.position(), end.position())

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        #grabs our start node and the current node
        current = open_set.get()[2]
        #removing the current node becasue we looked at it
        open_set_hash.remove(current)

        if current == end:
            #allows us to draw out the path
            path(came_from, current, draw)
            current.make_end()
            return True

        for neighbor in current.neighbors:
            t_g_score = g_score[neighbor] + 1

            if t_g_score < g_score[neighbor]:
                #making our path
                came_from[neighbor] = current 
                #updating the g_score of the neighbor nodes
                g_score[neighbor] = t_g_score
                #adding up the g_score and h function
                f_score[neighbor] = g_score + h(start.position(), end.position())
            #putting the neighbor into the open set 
            if neighbor not in open_set_hash:
                count +=1
                open_set.put((f_score[neighbor], count, neighbor))
                open_set_hash.add(neighbor)
                #giving it the open color
                neighbor.make_open()
        # calling the draw function that we are taking as an argument        
        draw()
        #the node has been looked at, make it red
        if current == start:
            current.make_closed()
    #end our while loop
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
        pygame.draw.line(surface, BLACK, (0, x * cube_size), (width, x * cube_size))
        for y in range(rows):
            #draws our lines for our y coordinates lines
            pygame.draw.line(surface, BLACK, (y * cube_size, 0), (y * cube_size, width))

def draw(surface, grid, rows, width):

    for row in grid:
        for node in row:
            node.draw(surface)
    draw_grid(surface, rows, width)
    pygame.display.update()
def main(surface, width):
    ROWS = 40
    game_on = True
    grid = make_grid(ROWS, width)
    start = None
    end = None

    while game_on:
        draw(surface, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

main(SURFACE, WIDTH)
