import pygame
import random
import math
import copy

# ------------------------------
# PARAMETERS
# ------------------------------
LOCUST_COUNT = 30
ITERATIONS = 200
NEIGHBORS = 3      # number of nearby locusts to consider
STEP = 1           # positions modified when moving
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
pygame.display.set_caption("Deliver-All-First Locust Swarm Optimization (LSO)")
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
# ROUTE FUNCTIONS
# ------------------------------
def total_distance(route, coords):
    total = 0
    full_route = [0] + route + [0]
    for i in range(len(full_route) - 1):
        total += math.hypot(coords[full_route[i]][0] - coords[full_route[i + 1]][0],
                            coords[full_route[i]][1] - coords[full_route[i + 1]][1])
    return total

def random_route(coords):
    route = list(range(1, len(coords)))
    random.shuffle(route)
    return route

def swap_move(route):
    """Perform a small random swap."""
    if len(route) < 2:
        return route[:]
    new_route = route[:]
    a, b = random.sample(range(len(route)), 2)
    new_route[a], new_route[b] = new_route[b], new_route[a]
    return new_route

# ------------------------------
# LOCUST SWARM FUNCTIONS
# ------------------------------
def lso_move(locust, population, coords, global_best):
    """Move toward global best or explore locally."""
    if random.random() < 0.7:
        # Move toward the global best (cohesion)
        new_locust = locust[:]
        if len(new_locust) > 1:
            i = random.randint(0, len(new_locust) - 1)
            new_locust[i] = global_best[i]
    else:
        # Random exploration
        new_locust = swap_move(locust)

    # Fix duplicates and missing cities
    seen, fixed = set(), []
    for c in new_locust:
        if c not in seen:
            fixed.append(c)
            seen.add(c)
    missing = list(set(global_best) - seen)
    fixed += missing
    return fixed

# ------------------------------
# VISUALIZATION
# ------------------------------
def draw_solution(route, coords, iteration, best_dist):
    screen.fill(WHITE)
    draw_grid()

    # Depot
    pygame.draw.circle(screen, RED, coords[0], 10)
    screen.blit(font.render("Depot", True, BLACK), (coords[0][0] + 10, coords[0][1] - 10))

    # Customers
    for i, (x, y) in enumerate(coords[1:], start=1):
        pygame.draw.circle(screen, BLUE, (x, y), 6)
        screen.blit(font.render(str(i), True, BLACK), (x + 5, y - 5))

    # Best route
    full_route = [0] + route + [0]
    for i in range(len(full_route) - 1):
        pygame.draw.line(screen, GREEN, coords[full_route[i]], coords[full_route[i + 1]], 3)

    # Info panel
    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
    text = f"Iteration: {iteration}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(text, True, BLACK), (20, SCREEN_SIZE + 30))
    pygame.display.flip()

# ------------------------------
# MAIN LSO LOOP
# ------------------------------
def lso_visual(coords):
    population = [random_route(coords) for _ in range(LOCUST_COUNT)]
    global_best = min(population, key=lambda l: total_distance(l, coords))
    best_dist = total_distance(global_best, coords)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        new_population = [lso_move(locust, population, coords, global_best) for locust in population]
        population = new_population

        current_best = min(population, key=lambda l: total_distance(l, coords))
        current_dist = total_distance(current_best, coords)
        if current_dist < best_dist:
            global_best = copy.deepcopy(current_best)
            best_dist = current_dist

        draw_solution(global_best, coords, iteration + 1, best_dist)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    print("\nFinal route:", [0] + global_best + [0])
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
    coords = [(SCREEN_SIZE // 2, SCREEN_SIZE // 2)]  # depot
    placing = True

    print("Click to add customer locations (snap to grid). Press ENTER to start LSO.")

    while placing:
        screen.fill(WHITE)
        draw_grid()

        # Depot
        pygame.draw.circle(screen, RED, coords[0], 10)
        screen.blit(font.render("Depot", True, BLACK), (coords[0][0] + 10, coords[0][1] - 10))

        # Customers
        for i, (x, y) in enumerate(coords[1:], start=1):
            pygame.draw.circle(screen, BLUE, (x, y), 6)
            screen.blit(font.render(str(i), True, BLACK), (x + 5, y - 5))

        pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
        msg = f"Customers: {len(coords) - 1} | Left-click to add, ENTER to start LSO"
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

    lso_visual(coords)

if __name__ == "__main__":
    main()
