import pygame
import random
import math
import copy

# ------------------------------
# PARAMETERS
# ------------------------------
CHEETAH_COUNT = 50
ITERATIONS = 500
CHASE_RATE = 0.7          # probability to chase better solution
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
pygame.display.set_caption("Deliver-All-First Cheetah Chase Algorithm")
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

def move_toward(route, target):
    new = route[:]
    for _ in range(STEP):
        i = random.randint(0, len(route) - 1)
        new[i] = target[i]

    # repair permutation
    seen, fixed = set(), []
    for c in new:
        if c not in seen:
            fixed.append(c)
            seen.add(c)
    missing = list(set(route) - seen)
    fixed.extend(missing)
    return fixed

# ------------------------------
# CCA OPERATORS
# ------------------------------
def chase_behavior(cheetah, population, global_best, coords):
    """Cheetah moves toward prey (better solution)."""
    if random.random() < CHASE_RATE:
        target = global_best
    else:
        target = random.choice(population)
    return move_toward(cheetah, target)

def sprint_mutation(cheetah, coords):
    """Small sprint or local mutation."""
    best = cheetah
    best_dist = total_distance(cheetah, coords)
    for _ in range(LOCAL_TRIALS):
        candidate = swap_mutation(cheetah)
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
# MAIN CCA LOOP
# ------------------------------
def cca_visual(coords):
    population = [random_route(coords) for _ in range(CHEETAH_COUNT)]
    global_best = min(population, key=lambda r: total_distance(r, coords))
    best_dist = total_distance(global_best, coords)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        new_population = []

        for cheetah in population:
            chased = chase_behavior(cheetah, population, global_best, coords)
            improved = sprint_mutation(chased, coords)
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

    print("Click to add customers (grid-snapped). Press ENTER to start Cheetah Chase Algorithm.")

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
        msg = f"Customers: {len(coords)-1} | ENTER to start Cheetah Chase Algorithm"
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

    cca_visual(coords)

if __name__ == "__main__":
    main()
