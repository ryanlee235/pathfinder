import pygame 
from queue import PriorityQueue

WIDTH = 600

SURFACE = pygame.display.set_mode((WIDTH))

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

def h(position1, position2):
    x1, x2 = position1
    y1, y2 = position2
    return abs(x1 - x2) + abs(y1 - y2)
    
               
def main(surface, width):
    ROWS = 40
    game_on = True

    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
