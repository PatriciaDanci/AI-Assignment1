from collections import deque
import heapq
import random
import pygame
import sys
import time

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

PASTEL_PINK = (255, 182, 193)
PASTEL_BLUE = (173, 216, 230)
PASTEL_PURPLE = (216, 191, 216)
PASTEL_GREEN = (152, 251, 152)
PASTEL_YELLOW = (255, 239, 213)
PASTEL_ORANGE = (255, 218, 185)
WHITE = (255, 255, 255)
GRID_LINE_COLOR = (200, 200, 200)
SAD_FACE_COLOR = (50, 50, 50)

EMPTY = WHITE
START = PASTEL_GREEN
GOAL = PASTEL_ORANGE
WALL = PASTEL_PURPLE
PATH = PASTEL_BLUE
VISITED = PASTEL_PINK

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")

grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
start = None
goal = None
costs = [[random.randint(1, 10) for _ in range(COLS)] for _ in range(ROWS)]  # costs for UCS, A Star and Dijkstra

def draw_grid():
    """Grid"""
    for row in range(ROWS):
        for col in range(COLS):
            color = grid[row][col]
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRID_LINE_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_cost_grid():
    """Same Grid but with Costs for algorithms that need it"""
    screen.fill(WHITE)  

    for row in range(ROWS):
        for col in range(COLS):
            color = grid[row][col]  # here we ensure the colors for start, goal and walls are kept
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRID_LINE_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            font = pygame.font.SysFont(None, 24)
            text = font.render(str(costs[row][col]), True, (0, 0, 0))
            text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
            screen.blit(text, text_rect)

    pygame.display.flip()

def draw_sad_face():
    """Grid with sad face for when an algorithm can't continue because it can't reach the other side of a wall"""
    for row in range(ROWS):
        for col in range(COLS):
            grid[row][col] = WHITE
            pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRID_LINE_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    
    sad_face_positions = [(8, 6), (8, 7), (8, 12), (8, 13), (9, 6), (9, 7), (9,12), (9, 13), (11, 9), (11, 10), (12, 8), (12, 11), (13, 7), (13, 12), (10, 5)]
    for (row, col) in sad_face_positions:
        pygame.draw.rect(screen, SAD_FACE_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    pygame.display.flip()
    time.sleep(5)

def get_clicked_pos(pos):
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

# DFS
def dfs(start, goal):
    stack = [(start, [])]  # Stack for current cell and path taken to reach it
    visited = set()  
    found_goal = False  # assume the goal hasn't been found yet

    while stack:
        (row, col), path = stack.pop()  

        if (row, col) == goal:
            print_path(path)
            for r, c in path:
                if (r, c) != start and (r, c) != goal:
                    grid[r][c] = PATH  
                    draw_grid()
                    pygame.display.flip()
                    time.sleep(0.05)
            found_goal = True
            break

        if (row, col) not in visited: # checks if the node hasn't been visited yet
            visited.add((row, col))
            grid[row][col] = VISITED
            draw_grid()
            pygame.display.flip()
            time.sleep(0.05)

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] #up, down, left, right

            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] in (EMPTY, GOAL) and (r, c) not in visited:
                    stack.append(((r, c), path + [(row, col)]))  # update path and add neighbor to the stack

    if not found_goal:
        draw_sad_face()  # displayed when the goal isn't reachable
        return False 

    return True  

# BFS 
def bfs(start, goal):
    queue = deque([(start, [])])  # Queue for current cell and path taken to reach it
    visited = set()  

    while queue:
        (row, col), path = queue.popleft() 

        if (row, col) == goal:
            print_path(path)
            for r, c in path:
                if (r, c) != start and (r, c) != goal:
                    grid[r][c] = PATH  
                    draw_grid()
                    pygame.display.flip()
                    time.sleep(0.05)
            return True 

        if (row, col) not in visited: # check to see if not visited
            visited.add((row, col)) # mark as visited
            grid[row][col] = VISITED
            draw_grid()
            pygame.display.flip()
            time.sleep(0.05)

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] #up, down, left, right
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] in (EMPTY, GOAL) and (r, c) not in visited:
                    queue.append(((r, c), path + [(row, col)]))  # enqueue the neighbor and update the path

    draw_sad_face() # displayed when the goal isn't reachable
    return False  

# UCS 
def ucs(start, goal):
    pq = []
    heapq.heappush(pq, (0, start, []))
    visited = set()

    while pq:
        cost, (row, col), path = heapq.heappop(pq)

        if (row, col) == goal:
            print_path(path)
            for r, c in path:
                if (r, c) != start and (r, c) != goal:
                    grid[r][c] = PATH
                    draw_grid() 
                    pygame.display.flip()
                    time.sleep(0.05)
            return True

        if (row, col) not in visited:
            visited.add((row, col))
            grid[row][col] = VISITED
            draw_grid() 
            pygame.display.flip()
            time.sleep(0.05)

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] != WALL and (r, c) not in visited:
                    move_cost = costs[r][c]
                    new_cost = cost + move_cost
                    heapq.heappush(pq, (new_cost, (r, c), path + [(row, col)]))

    draw_sad_face() # displayed when the goal isn't reachable
    return False

def heuristic(cell, goal):
    """Heuristic function for A* (Manhattan distance)."""
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

#A star 
def a_star(start, goal):
    pq = []
    heapq.heappush(pq, (0, start, []))  # Priority queue with (f_cost, cell, path)
    g_cost = {start: 0}  # cost from start to each cell
    visited = set()

    while pq:
        f_cost, (row, col), path = heapq.heappop(pq)

        if (row, col) == goal:
            print_path(path)
            for r, c in path:
                if (r, c) != start and (r, c) != goal:
                    grid[r][c] = PATH
                    draw_grid()
                    pygame.display.flip()
                    time.sleep(0.05)
            return True

        if (row, col) not in visited:
            visited.add((row, col))
            grid[row][col] = VISITED
            draw_grid()
            pygame.display.flip()
            time.sleep(0.05)

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] != WALL:
                    new_g_cost = g_cost[(row, col)] + costs[r][c]
                    if (r, c) not in g_cost or new_g_cost < g_cost[(r, c)]:
                        g_cost[(r, c)] = new_g_cost
                        h_cost = heuristic((r, c), goal)
                        new_f_cost = new_g_cost + h_cost
                        heapq.heappush(pq, (new_f_cost, (r, c), path + [(row, col)]))

    draw_sad_face() # displayed when the goal isn't reachable
    return False

#Dijkstra 
def dijkstra(start, goal):
    pq = []
    heapq.heappush(pq, (0, start, []))  # Priority queue with (cost, cell, path)
    visited = set()
    g_cost = {start: 0}  

    while pq:
        cost, (row, col), path = heapq.heappop(pq)

        if (row, col) == goal:
            print_path(path)
            for r, c in path:
                if (r, c) != start and (r, c) != goal:
                    grid[r][c] = PATH
                    draw_grid()  
                    pygame.display.flip()
                    time.sleep(0.05)
            return True

        if (row, col) not in visited:
            visited.add((row, col))
            grid[row][col] = VISITED
            draw_grid() 
            pygame.display.flip()
            time.sleep(0.05)

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] != WALL:
                    new_cost = g_cost[(row, col)] + costs[r][c]
                    if (r, c) not in g_cost or new_cost < g_cost[(r, c)]:
                        g_cost[(r, c)] = new_cost
                        heapq.heappush(pq, (new_cost, (r, c), path + [(row, col)]))

    draw_sad_face() # displayed when the goal isn't reachable
    return False

def print_path(path):
    """Print the path in the specified format."""
    print("Path")
    print("Start:")
    for step in path:
        print(f"  {step},")
    print("Goal")
    print(f"Length: {len(path)} steps\n")

def main():
    global start, goal
    running = True
    show_cost_grid = False  

    while running:
        if not show_cost_grid:
            screen.fill(WHITE)
            draw_grid()
        else:
            draw_cost_grid() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                if not start:
                    start = (row, col)
                    grid[row][col] = START
                elif not goal and (row, col) != start:
                    goal = (row, col)
                    grid[row][col] = GOAL
                elif (row, col) != start and (row, col) != goal:
                    grid[row][col] = WALL

            elif pygame.mouse.get_pressed()[2]:  # Right mouse button to reset cell
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                if (row, col) == start:
                    start = None
                elif (row, col) == goal:
                    goal = None
                grid[row][col] = EMPTY

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and start and goal:
                    dfs(start, goal)  # Run DFS 
                elif event.key == pygame.K_b and start and goal:
                    bfs(start, goal)  # Run BFS 
                elif event.key == pygame.K_g and start and goal:
                    show_cost_grid = True  # Enable cost grid display
                    draw_cost_grid() 
                elif event.key == pygame.K_u and start and goal:
                    ucs(start, goal)  # Run UCS 
                elif event.key == pygame.K_a  and start and goal:
                    a_star(start, goal)  # Run A* 
                elif event.key == pygame.K_k  and start and goal:
                    dijkstra(start, goal) #Run Dijkstra 
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
