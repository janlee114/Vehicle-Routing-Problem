import pygame
import random
import math
import copy

# ------------------------------
# PARAMETERS
# ------------------------------
CUCKOO_COUNT = 30
ITERATIONS = 200
ABANDON_RATE = 0.50   # fraction of nests to abandon
STEP = 1              # number of swaps per Lévy-like flight
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
pygame.display.set_caption("Deliver-All-First Cuckoo Optimization Algorithm (COA)")
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
# ROUTE UTILITIES
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

def levy_flight_mutation(route):
    """Perform a Lévy-like mutation (multiple small swaps)."""
    new_route = route[:]
    for _ in range(STEP):
        if len(new_route) > 1:
            a, b = random.sample(range(len(new_route)), 2)
            new_route[a], new_route[b] = new_route[b], new_route[a]
    return new_route

# ------------------------------
# COA FUNCTIONS
# ------------------------------
def generate_egg(cuckoo, coords):
    """Create a new solution (egg) by Lévy-style mutation around a parent cuckoo."""
    new_egg = levy_flight_mutation(cuckoo)
    return new_egg

def replace_worst(population, coords, abandon_rate):
    """Replace a fraction of worst nests with random routes."""
    population.sort(key=lambda r: total_distance(r, coords))
    cutoff = int(len(population) * (1 - abandon_rate))
    survivors = population[:cutoff]
    new_nests = [random_route(coords) for _ in range(len(population) - cutoff)]
    return survivors + new_nests

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

    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
    text = f"Iteration: {iteration}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(text, True, BLACK), (20, SCREEN_SIZE + 30))
    pygame.display.flip()

# ------------------------------
# MAIN COA LOOP
# ------------------------------
def coa_visual(coords):
    population = [random_route(coords) for _ in range(CUCKOO_COUNT)]
    global_best = min(population, key=lambda c: total_distance(c, coords))
    best_dist = total_distance(global_best, coords)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        # Generate eggs (new candidates)
        eggs = [generate_egg(c, coords) for c in population]
        combined = population + eggs

        # Keep best solutions and replace worst nests
        combined.sort(key=lambda r: total_distance(r, coords))
        combined = replace_worst(combined, coords, ABANDON_RATE)

        population = combined
        current_best = min(population, key=lambda c: total_distance(c, coords))
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

    print("Click to add customer locations (snap to grid). Press ENTER to start COA.")

    while placing:
        screen.fill(WHITE)
        draw_grid()

        pygame.draw.circle(screen, RED, coords[0], 10)
        screen.blit(font.render("Depot", True, BLACK), (coords[0][0] + 10, coords[0][1] - 10))

        for i, (x, y) in enumerate(coords[1:], start=1):
            pygame.draw.circle(screen, BLUE, (x, y), 6)
            screen.blit(font.render(str(i), True, BLACK), (x + 5, y - 5))

        pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
        msg = f"Customers: {len(coords) - 1} | Left-click to add, ENTER to start COA"
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

    coa_visual(coords)

if __name__ == "__main__":
    main()
