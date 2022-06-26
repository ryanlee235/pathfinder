import pygame 

WIDTH, HEIGHT = 800, 800

SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder")
#NODES CHECKED COLOR
RED = (255, 0, 0)
#START NODE
BLUE = (0, 255, 0)
#LINES
GRAY = (128, 128, 128)
#PATH
PURPLE =(128, 0, 128)
#END NODE
TEAL = (0, 128, 128)
#BARRIER
BLACK = (0, 0, 0)
#BACK GROUND
WHITE = (255, 255, 255)

class Node:
    def __init(self, width, height, rows, col, TotalRows):
        self.color = WHITE
        self.rows = rows
        self.col = col
        self.x = rows * width 
        self.y = col * height
        self.TotalRows = TotalRows
        self.open_list = []

    def start_node_color(self):
        return self.color == BLUE
    
    def end_node_color(self):
        return self.color == TEAL
    
    def barrier_color(self):
        return self.color == BLACK
    
    def path_color(self):
        return self.color == PURPLE

    def nodes_checked(self):
        return self.color == RED
    
    def make_start_node(self):
        self.color = BLUE

    def make_end_node(self):
        self.color = TEAL

    def make_barrier(self):
        self.color = BLACK
    
    def make_path(self):
        self.color = PURPLE
    
    def make_nodes_checked(self):
        self.color = RED

    def neighbor_nodes(self):
        pass

    def draw_squares(self, surface):
        pass

    
