import pygame
import random
import math
import copy

# ------------------------------
# PARAMETERS
# ------------------------------
MUSHROOM_COUNT = 30
ITERATIONS = 200
SPORE_RATE = 0.6          # Probability to release new spores around best mushroom
LOCAL_TRIALS = 5
STEP = 1
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
pygame.display.set_caption("Deliver-All-First Mushroom Reproduction Optimization (MRO)")
font = pygame.font.SysFont("Arial", 20)

# ------------------------------
# GRID & SNAP
# ------------------------------
def snap_to_grid(x, y):
    return round(x / GRID_SPACING) * GRID_SPACING, round(y / GRID_SPACING) * GRID_SPACING

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
    full = [0] + route + [0]
    for i in range(len(full) - 1):
        total += math.hypot(
            coords[full[i]][0] - coords[full[i + 1]][0],
            coords[full[i]][1] - coords[full[i + 1]][1]
        )
    return total

def random_route(coords):
    r = list(range(1, len(coords)))
    random.shuffle(r)
    return r

def swap_mutation(route):
    if len(route) < 2:
        return route[:]
    r = route[:]
    i, j = random.sample(range(len(r)), 2)
    r[i], r[j] = r[j], r[i]
    return r

def combine_routes(parent1, parent2):
    """Reproduction mechanism – combine parts of two parents."""
    cut = random.randint(1, len(parent1) - 1)
    child = parent1[:cut] + [c for c in parent2 if c not in parent1[:cut]]
    return child

# ------------------------------
# MRO OPERATORS
# ------------------------------
def release_spores(mushroom, population, global_best):
    """Each mushroom releases spores — either near global best or local neighbor."""
    if random.random() < SPORE_RATE:
        parent2 = global_best
    else:
        parent2 = random.choice(population)
    return combine_routes(mushroom, parent2)

def local_improvement(route, coords):
    best = route
    best_dist = total_distance(route, coords)
    for _ in range(LOCAL_TRIALS):
        candidate = swap_mutation(route)
        d = total_distance(candidate, coords)
        if d < best_dist:
            best = candidate
            best_dist = d
    return best

# ------------------------------
# VISUALIZATION
# ------------------------------
def draw_solution(route, coords, iteration, best_dist):
    screen.fill(WHITE)
    draw_grid()

    # Depot
    pygame.draw.circle(screen, RED, coords[0], 10)
    screen.blit(font.render("Depot", True, BLACK),
                (coords[0][0] + 10, coords[0][1] - 10))

    # Customers
    for i, (x, y) in enumerate(coords[1:], start=1):
        pygame.draw.circle(screen, BLUE, (x, y), 6)
        screen.blit(font.render(str(i), True, BLACK), (x + 5, y - 5))

    # Route
    full = [0] + route + [0]
    for i in range(len(full) - 1):
        pygame.draw.line(screen, GREEN, coords[full[i]], coords[full[i + 1]], 3)

    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
    text = f"Iteration: {iteration}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(text, True, BLACK), (20, SCREEN_SIZE + 30))
    pygame.display.flip()

# ------------------------------
# MAIN MRO LOOP
# ------------------------------
def mro_visual(coords):
    population = [random_route(coords) for _ in range(MUSHROOM_COUNT)]
    global_best = min(population, key=lambda r: total_distance(r, coords))
    best_dist = total_distance(global_best, coords)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        new_population = []

        for mushroom in population:
            spore = release_spores(mushroom, population, global_best)
            improved = local_improvement(spore, coords)
            new_population.append(improved)

        population = new_population
        current_best = min(population, key=lambda r: total_distance(r, coords))
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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.time.wait(100)

# ------------------------------
# MAIN
# ------------------------------
def main():
    coords = [(SCREEN_SIZE // 2, SCREEN_SIZE // 2)]
    placing = True

    print("Click to add customers (grid-snapped). Press ENTER to start Mushroom Reproduction Optimization.")

    while placing:
        screen.fill(WHITE)
        draw_grid()

        # Draw depot
        pygame.draw.circle(screen, RED, coords[0], 10)
        screen.blit(font.render("Depot", True, BLACK), (coords[0][0] + 10, coords[0][1] - 10))

        # Draw customers
        for i, (x, y) in enumerate(coords[1:], start=1):
            pygame.draw.circle(screen, BLUE, (x, y), 6)
            screen.blit(font.render(str(i), True, BLACK), (x + 5, y - 5))

        # Interface info
        pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
        msg = f"Customers: {len(coords)-1} | ENTER to start MRO"
        screen.blit(font.render(msg, True, BLACK), (20, SCREEN_SIZE + 30))
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if y < SCREEN_SIZE:
                    coords.append(snap_to_grid(x, y))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                placing = False

    mro_visual(coords)

if __name__ == "__main__":
    main()
