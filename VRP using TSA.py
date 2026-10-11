import pygame
import random
import math
from collections import deque

# ------------------------------
# PARAMETERS
# ------------------------------
TABU_TENURE = 15
ITERATIONS = 300
NEIGHBORS_PER_ITER = 50
SCREEN_SIZE = 700
GRID_SPACING = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 30, 30)
BLUE = (30, 30, 200)
GREEN = (30, 200, 30)
GRAY = (160, 160, 160)
LIGHT_GRAY = (220, 220, 220)

# ------------------------------
# PYGAME INIT
# ------------------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 100))
pygame.display.set_caption("Deliver-All-First Tabu Search")
font = pygame.font.SysFont("Arial", 20)

# ------------------------------
# GRID & SNAP
# ------------------------------
def snap_to_grid(x, y):
    gx = round(x / GRID_SPACING) * GRID_SPACING
    gy = round(y / GRID_SPACING) * GRID_SPACING
    return gx, gy

def draw_grid():
    for x in range(0, SCREEN_SIZE, GRID_SPACING):
        pygame.draw.line(screen, LIGHT_GRAY, (x, 0), (x, SCREEN_SIZE))
    for y in range(0, SCREEN_SIZE, GRID_SPACING):
        pygame.draw.line(screen, LIGHT_GRAY, (0, y), (SCREEN_SIZE, y))

# ------------------------------
# VRP UTILS
# ------------------------------
def total_distance(route, coords):
    total = 0
    full_route = [0] + route + [0]
    for i in range(len(full_route)-1):
        total += math.hypot(coords[full_route[i]][0]-coords[full_route[i+1]][0],
                            coords[full_route[i]][1]-coords[full_route[i+1]][1])
    return total

def get_neighbors(route, num_neighbors=50):
    neighbors = []
    n = len(route)
    for _ in range(num_neighbors):
        i, j = random.sample(range(n), 2)
        neighbor = route[:]
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbors.append(((i,j), neighbor))
    return neighbors

# ------------------------------
# PYGAME VISUALIZATION
# ------------------------------
def draw_solution(route, coords, iteration, best_dist):
    screen.fill(WHITE)
    draw_grid()

    # Depot
    pygame.draw.circle(screen, RED, coords[0], 10)
    screen.blit(font.render("Depot", True, BLACK), (coords[0][0]+10, coords[0][1]-10))

    # Customers
    for i, (x, y) in enumerate(coords[1:], start=1):
        pygame.draw.circle(screen, BLUE, (x, y), 6)
        screen.blit(font.render(str(i), True, BLACK), (x+5, y-5))

    # Draw route
    full_route = [0] + route + [0]
    for i in range(len(full_route)-1):
        pygame.draw.line(screen, GREEN, coords[full_route[i]], coords[full_route[i+1]], 3)

    # Info panel
    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
    text = f"Iteration: {iteration}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(text, True, BLACK), (20, SCREEN_SIZE+30))
    pygame.display.flip()

# ------------------------------
# TABU SEARCH MAIN LOOP
# ------------------------------
def tabu_search_visual(coords):
    # initial solution
    route = list(range(1, len(coords)))
    best_route = route[:]
    best_dist = total_distance(best_route, coords)

    tabu_list = deque(maxlen=TABU_TENURE)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        neighbors = get_neighbors(route, NEIGHBORS_PER_ITER)
        neighbors.sort(key=lambda x: total_distance(x[1], coords))

        for move, candidate in neighbors:
            if move not in tabu_list or total_distance(candidate, coords) < best_dist:
                route = candidate
                tabu_list.append(move)
                break

        current_dist = total_distance(route, coords)
        if current_dist < best_dist:
            best_route = route[:]
            best_dist = current_dist

        draw_solution(best_route, coords, iteration+1, best_dist)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    print("\nFinal route:", [0]+best_route+[0])
    print("Total distance:", best_dist)

    # Keep window open
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
        pygame.time.wait(100)

    pygame.quit()

# ------------------------------
# MAIN EXECUTION
# ------------------------------
def main():
    coords = [(SCREEN_SIZE//2, SCREEN_SIZE//2)]  # depot
    placing = True

    print("Click to add customer locations (snapped to grid). Press ENTER to start Tabu Search.")

    while placing:
        screen.fill(WHITE)
        draw_grid()

        # Draw depot
        pygame.draw.circle(screen, RED, coords[0], 10)
        screen.blit(font.render("Depot", True, BLACK), (coords[0][0]+10, coords[0][1]-10))

        # Draw points
        for i, (x, y) in enumerate(coords[1:], start=1):
            pygame.draw.circle(screen, BLUE, (x, y), 6)
            screen.blit(font.render(str(i), True, BLACK), (x+5, y-5))

        pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
        msg = f"Customers: {len(coords)-1} | Left-click to add, ENTER to start"
        screen.blit(font.render(msg, True, BLACK), (20, SCREEN_SIZE+30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if y < SCREEN_SIZE:
                    gx, gy = snap_to_grid(x, y)
                    coords.append((gx, gy))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                placing = False

    tabu_search_visual(coords)

if __name__ == "__main__":
    main()
