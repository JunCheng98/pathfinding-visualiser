import pygame
import math

from queue import PriorityQueue, Queue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinders")

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

# Represents each node in the grid
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.colour == RED
    
    def is_open(self):
        return self.colour == GREEN

    def is_barrier(self):
        return self.colour == BLACK

    def is_start(self):
        return self.colour == ORANGE

    def is_end(self):
        return self.colour == PURPLE

    def reset(self):
        self.colour = WHITE

    def make_closed(self):
        self.colour = RED
    
    def make_open(self):
        self.colour = GREEN

    def make_barrier(self):
        self.colour = BLACK

    def make_start(self):
        self.colour = ORANGE

    def make_end(self):
        self.colour = PURPLE

    def make_path(self):
        self.colour = TURQUOISE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        return False

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
    
# heuristic for A* algorithm (manhattan distance)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# A* algorithm
def astar(draw, grid, start, end):
    count = 0
    frontier = PriorityQueue()
    
    frontier.put((0, count, start))
    came_from = {}
    
    # actual cost up to current node from the start
    g_value = {node: float("inf") for row in grid for node in row}
    g_value[start] = 0

    # total cost to goal node, sum of g(n) and h(n)
    f_value = {node: float("inf") for row in grid for node in row}
    f_value[start] = h(start.get_pos(), end.get_pos()) # g(n) = 0

    frontier_copy = {start}

    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # get the current node with lowest f(n)
        current = frontier.get()[2]
        frontier_copy.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbour in current.neighbours:
            temp_g = g_value[current] + 1

            if temp_g < g_value[neighbour]:
                came_from[neighbour] = current
                g_value[neighbour] = temp_g
                f_value[neighbour] = temp_g + h(neighbour.get_pos(), end.get_pos())

                if neighbour not in frontier_copy:
                    count += 1
                    frontier.put((f_value[neighbour], count, neighbour))
                    frontier_copy.add(neighbour)
                    neighbour.make_open()
                    
        draw()

        if current != start:
            current.make_closed()

    return False

def bfs(draw, grid, start, end):
    frontier = Queue()
    frontier.put(start)
    came_from = {}

    visited = {start}

    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = frontier.get()

        for neighbour in current.neighbours:
            if neighbour == end:
                came_from[neighbour] = current
                reconstruct_path(came_from, end, draw)
                end.make_end()
                start.make_start()
                return True
            
            if neighbour not in visited:
                came_from[neighbour] = current
                frontier.put(neighbour)
                visited.add(neighbour)
                neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


# initialises the grid
def make_grid(rows, width): # TODO: change length
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

# draws horizontal and vertical lines to form grids
def draw_grid(win, rows, width): # TODO: change length
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Main drawing driver
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

# find the position where the mouse clicked on the grid
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    # TODO
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        # detect all events that happen in window
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != start and node != end:
                    node.make_barrier()
            
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                
                if node == start:
                    start = None
                elif node == end:
                    end = None

            # TODO: use button clicking to trigger this, and disable clicking until algo finishes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

                #TODO: add dijkstra and weighted tiles

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    # TODO
                    grid = make_grid(ROWS, width)


    pygame.quit()

# run the program (remember to make space at top for other stuff later)
main(WIN, WIDTH)