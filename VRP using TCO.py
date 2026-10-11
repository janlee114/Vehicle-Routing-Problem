import pygame
import random
import math
import copy

# ------------------------------
# PARAMETERS
# ------------------------------
TERMITE_COUNT = 30
ITERATIONS = 200
PHEROMONE_INIT = 1.0
EVAPORATION = 0.05
ALPHA = 1.0   # pheromone influence
BETA = 3.0    # distance influence
Q = 100.0     # pheromone reinforcement factor
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
pygame.display.set_caption("Deliver-All-First Termite Colony Optimization (TCO)")
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
# DISTANCE MATRIX
# ------------------------------
def calc_dist_matrix(coords):
    n = len(coords)
    dist = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = math.hypot(coords[i][0]-coords[j][0],
                                        coords[i][1]-coords[j][1])
    return dist

# ------------------------------
# TOTAL DISTANCE
# ------------------------------
def total_distance(route, coords):
    total = 0
    full_route = [0] + route + [0]
    for i in range(len(full_route)-1):
        total += math.hypot(coords[full_route[i]][0]-coords[full_route[i+1]][0],
                            coords[full_route[i]][1]-coords[full_route[i+1]][1])
    return total

# ------------------------------
# TERMITE ROUTE CONSTRUCTION
# ------------------------------
def build_route(coords, pheromone, dist):
    n = len(coords)
    route = []
    visited = [False]*n
    current = 0
    visited[current] = True

    while len(route) < n-1:
        unvisited = [i for i in range(1, n) if not visited[i]]
        if not unvisited:
            break

        # Probabilities based on pheromone and inverse distance
        probs = []
        for j in unvisited:
            tau = pheromone[current][j] ** ALPHA
            eta = (1.0 / (dist[current][j] + 1e-9)) ** BETA
            probs.append(tau * eta)
        s = sum(probs)
        probs = [p/s for p in probs]
        next_city = random.choices(unvisited, weights=probs)[0]
        route.append(next_city)
        visited[next_city] = True
        current = next_city

    return route

# ------------------------------
# PHEROMONE UPDATE
# ------------------------------
def update_pheromones(pheromone, termites, coords):
    # Evaporation
    n = len(pheromone)
    for i in range(n):
        for j in range(n):
            pheromone[i][j] *= (1 - EVAPORATION)
            if pheromone[i][j] < 1e-6:
                pheromone[i][j] = 1e-6

    # Reinforcement
    for route in termites:
        length = total_distance(route, coords)
        deposit = Q / length
        full_route = [0] + route + [0]
        for i in range(len(full_route)-1):
            a, b = full_route[i], full_route[i+1]
            pheromone[a][b] += deposit
            pheromone[b][a] += deposit

# ------------------------------
# VISUALIZATION
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

    # Best route
    full_route = [0] + route + [0]
    for i in range(len(full_route)-1):
        pygame.draw.line(screen, GREEN, coords[full_route[i]], coords[full_route[i+1]], 3)

    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
    text = f"Iteration: {iteration}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(text, True, BLACK), (20, SCREEN_SIZE + 30))
    pygame.display.flip()

# ------------------------------
# MAIN TCO LOOP
# ------------------------------
def tco_visual(coords):
    n = len(coords)
    dist = calc_dist_matrix(coords)
    pheromone = [[PHEROMONE_INIT for _ in range(n)] for _ in range(n)]

    best_route = random.sample(range(1, n), n-1)
    best_dist = total_distance(best_route, coords)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        termites = [build_route(coords, pheromone, dist) for _ in range(TERMITE_COUNT)]
        update_pheromones(pheromone, termites, coords)

        current_best = min(termites, key=lambda r: total_distance(r, coords))
        current_dist = total_distance(current_best, coords)

        if current_dist < best_dist:
            best_route = copy.deepcopy(current_best)
            best_dist = current_dist

        draw_solution(best_route, coords, iteration+1, best_dist)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    print("\nFinal route:", [0] + best_route + [0])
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

    print("Click to add customer locations (snap to grid). Press ENTER to start TCO.")

    while placing:
        screen.fill(WHITE)
        draw_grid()

        pygame.draw.circle(screen, RED, coords[0], 10)
        screen.blit(font.render("Depot", True, BLACK), (coords[0][0]+10, coords[0][1]-10))

        for i, (x, y) in enumerate(coords[1:], start=1):
            pygame.draw.circle(screen, BLUE, (x, y), 6)
            screen.blit(font.render(str(i), True, BLACK), (x+5, y-5))

        pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
        msg = f"Customers: {len(coords)-1} | Left-click to add, ENTER to start TCO"
        screen.blit(font.render(msg, True, BLACK), (20, SCREEN_SIZE + 30))
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

    tco_visual(coords)

if __name__ == "__main__":
    main()
