import pygame
import random
import math

# ------------------------------
# PARAMETERS
# ------------------------------
NUM_ANTS = 30
ITERATIONS = 200
ALPHA = 1.0       # pheromone influence
BETA = 5.0        # distance influence
EVAPORATION = 0.5
Q = 100           # pheromone deposit factor
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
pygame.display.set_caption("Deliver-All-First Ant Colony Optimization")
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
def distance(a, b, coords):
    return math.hypot(coords[a][0]-coords[b][0], coords[a][1]-coords[b][1])

def total_distance(route, coords):
    total = 0
    full_route = [0] + route + [0]
    for i in range(len(full_route)-1):
        total += distance(full_route[i], full_route[i+1], coords)
    return total

def choose_next_node(current, unvisited, pheromone, coords):
    denom = 0
    probs = []
    for node in unvisited:
        denom += (pheromone[current][node] ** ALPHA) * ((1.0 / distance(current, node, coords)) ** BETA)
    for node in unvisited:
        prob = ((pheromone[current][node] ** ALPHA) * ((1.0 / distance(current, node, coords)) ** BETA)) / denom
        probs.append((node, prob))
    r = random.random()
    cumulative = 0
    for node, prob in probs:
        cumulative += prob
        if r <= cumulative:
            return node
    return probs[-1][0]

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
# ACO MAIN LOOP
# ------------------------------
def ant_colony_optimization_visual(coords):
    n = len(coords)
    pheromone = [[1.0 for _ in range(n)] for _ in range(n)]
    best_route = list(range(1, n))
    best_dist = total_distance(best_route, coords)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        all_routes = []
        all_lengths = []

        for _ in range(NUM_ANTS):
            unvisited = set(range(1, n))
            current = 0
            route = []
            while unvisited:
                next_node = choose_next_node(current, unvisited, pheromone, coords)
                route.append(next_node)
                unvisited.remove(next_node)
                current = next_node
            all_routes.append(route)
            all_lengths.append(total_distance(route, coords))

        # Update best
        min_idx = all_lengths.index(min(all_lengths))
        if all_lengths[min_idx] < best_dist:
            best_dist = all_lengths[min_idx]
            best_route = all_routes[min_idx][:]

        # Pheromone evaporation
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1 - EVAPORATION)
                if pheromone[i][j] < 0.01:
                    pheromone[i][j] = 0.01

        # Deposit pheromone
        for route, length in zip(all_routes, all_lengths):
            for i in range(len(route)):
                a = 0 if i==0 else route[i-1]
                b = route[i]
                pheromone[a][b] += Q / length
                pheromone[b][a] += Q / length

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

    print("Click to add customer locations (snapped to grid). Press ENTER to start ACO.")

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

    ant_colony_optimization_visual(coords)

if __name__ == "__main__":
    main()
