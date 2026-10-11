import pygame
import random
import math
import copy

# ------------------------------
# PARAMETERS
# ------------------------------
COCKROACH_COUNT = 30
ITERATIONS = 200
SOCIAL_RADIUS = 5    # number of neighbors to consider
STEP = 1             # positions changed during movement
SCREEN_SIZE = 700
GRID_SPACING = 50
FOLLOW_RATE = 0.7    # probability of moving toward better cockroach
DISPERSAL_RATE = 0.3 # probability of random dispersal

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
pygame.display.set_caption("Deliver-All-First Cockroach Swarm Optimization (CSO)")
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

def swap_move(route):
    """Perform a small random swap mutation."""
    if len(route) < 2:
        return route[:]
    new_route = route[:]
    a, b = random.sample(range(len(route)), 2)
    new_route[a], new_route[b] = new_route[b], new_route[a]
    return new_route

# ------------------------------
# CSO FUNCTIONS
# ------------------------------
def cso_move(cockroach, population, coords, global_best):
    """Each cockroach follows or disperses."""
    if random.random() < FOLLOW_RATE:
        # Follow better neighbor
        neighbors = random.sample(population, min(SOCIAL_RADIUS, len(population)))
        better = [n for n in neighbors if total_distance(n, coords) < total_distance(cockroach, coords)]
        if better:
            target = random.choice(better)
        else:
            target = global_best
        new_cockroach = follow_route(cockroach, target)
    elif random.random() < DISPERSAL_RATE:
        # Random dispersal
        new_cockroach = swap_move(cockroach)
    else:
        # Move slightly toward global best
        new_cockroach = follow_route(cockroach, global_best)
    return new_cockroach

def follow_route(cockroach, target):
    """Move partially toward a target route."""
    new_route = cockroach[:]
    if len(new_route) > 1:
        for _ in range(STEP):
            i = random.randint(0, len(new_route) - 1)
            new_route[i] = target[i]
    # Fix duplicates and missing nodes
    seen, fixed = set(), []
    for c in new_route:
        if c not in seen:
            fixed.append(c)
            seen.add(c)
    missing = list(set(target) - seen)
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

    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
    text = f"Iteration: {iteration}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(text, True, BLACK), (20, SCREEN_SIZE + 30))
    pygame.display.flip()

# ------------------------------
# MAIN CSO LOOP
# ------------------------------
def cso_visual(coords):
    population = [random_route(coords) for _ in range(COCKROACH_COUNT)]
    global_best = min(population, key=lambda c: total_distance(c, coords))
    best_dist = total_distance(global_best, coords)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        new_population = [cso_move(c, population, coords, global_best) for c in population]
        population = new_population

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

    print("Click to add customer locations (snap to grid). Press ENTER to start CSO.")

    while placing:
        screen.fill(WHITE)
        draw_grid()

        pygame.draw.circle(screen, RED, coords[0], 10)
        screen.blit(font.render("Depot", True, BLACK), (coords[0][0] + 10, coords[0][1] - 10))

        for i, (x, y) in enumerate(coords[1:], start=1):
            pygame.draw.circle(screen, BLUE, (x, y), 6)
            screen.blit(font.render(str(i), True, BLACK), (x + 5, y - 5))

        pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
        msg = f"Customers: {len(coords) - 1} | Left-click to add, ENTER to start CSO"
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

    cso_visual(coords)

if __name__ == "__main__":
    main()

