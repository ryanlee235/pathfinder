import pygame 

WIDTH = 800 
HIGHT = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
#barrier color
BLACK = (0, 0, 0)
#reguar color block
WHITE = (255, 255, 255)
#node color that has already been searched
RED = (255, 0, 0)
# start node color
GREEN = (0, 128, 0)
#path color
PURPLE = (128, 0, 128)
# end node color
TEAL = (0, 128, 128)
#open list color
BLUE =(0, 0, 255)

class Node:
    def __init__(self, rows, col, width, total_rows):
        self.rows = rows 
        self.col = col 
        #gets x position
        self.x = rows * width
        #gets y position 
        self.y = col * width
        #going to get all the adjacent cells next to our start nodes 
        self.open_list = []
        #going to use for our h function later
        self.total_rows = total_rows
        self.color = WHITE
    def pos(self):
        #gets the current position 
        return self.rows, self.col 

    def barrier_color(self):
        return self.color == BLACK
         
    def open_color(self):
        return self.color == BLUE

    def closed_color(self):
        return self.color == RED

    def start_color(self):
        return self.color == GREEN

    def end_color(self):
        return self.color == TEAL

    def path_color(self):
        return self.color == PURPLE

    def barrier(self):
        self.color = BLACK
    
    def open(self):
        self.color = BLUE

    def closed(self):
        self.color = RED 
    
    def start(self):
        self.color = GREEN

    def end(self):
        self.color = TEAL
    
    def path(self):
        self.color = PURPLE

    def open_list(self):
        #this is going to contain the up, down, right, left of the start node
        open_list = []
#this gets manhattan distances.
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)



def draw_grid():
    WIN.fill(BLACK)
    pygame.display.update()

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_grid()

    pygame.quit()

       


if __name__ == '__main__':
    main()
