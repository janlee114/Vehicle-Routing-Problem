import pygame
import random
import math
import copy

# ------------------------------
# PARAMETERS
# ------------------------------
BEE_COUNT = 20
ITERATIONS = 150
RECRUIT_RATIO = 0.5  # fraction of best bees that can recruit others
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
pygame.display.set_caption("Deliver-All-First Bee Colony Optimization (BCO)")
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

# ------------------------------
# BCO ALGORITHM FUNCTIONS
# ------------------------------
def forward_pass(coords):
    """Each bee constructs a route step-by-step."""
    route = []
    unvisited = list(range(1, len(coords)))
    current = 0  # start from depot
    while unvisited:
        next_node = random.choice(unvisited)
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node
    return route

def recruit(bees, coords):
    """Recruitment: best bees attract others."""
    bees_sorted = sorted(bees, key=lambda r: total_distance(r, coords))
    best_count = max(1, int(len(bees) * RECRUIT_RATIO))
    best_bees = bees_sorted[:best_count]

    new_bees = []
    for bee in bees:
        if bee not in best_bees:
            recruiter = random.choice(best_bees)
            adopt_len = len(recruiter)//2
            new_route = recruiter[:adopt_len]
            for c in bee:
                if c not in new_route:
                    new_route.append(c)
            new_bees.append(new_route)
        else:
            new_bees.append(bee)
    return new_bees

# ------------------------------
# PYGAME VISUALIZATION
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

    # Route
    full_route = [0] + route + [0]
    for i in range(len(full_route) - 1):
        pygame.draw.line(screen, GREEN, coords[full_route[i]], coords[full_route[i + 1]], 3)

    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
    text = f"Iteration: {iteration}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(text, True, BLACK), (20, SCREEN_SIZE + 30))
    pygame.display.flip()

# ------------------------------
# MAIN BCO LOOP
# ------------------------------
def bco_visual(coords):
    # Initialize bees
    bees = [forward_pass(coords) for _ in range(BEE_COUNT)]
    best_bee = min(bees, key=lambda r: total_distance(r, coords))
    best_dist = total_distance(best_bee, coords)

    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        # Forward pass (each bee constructs new solution)
        bees = [forward_pass(coords) for _ in range(BEE_COUNT)]

        # Recruitment (best bees attract others)
        bees = recruit(bees, coords)

        # Update best solution
        current_best = min(bees, key=lambda r: total_distance(r, coords))
        current_dist = total_distance(current_best, coords)
        if current_dist < best_dist:
            best_bee = copy.deepcopy(current_best)
            best_dist = current_dist

        draw_solution(best_bee, coords, iteration + 1, best_dist)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    print("\nFinal route:", [0] + best_bee + [0])
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

    print("Click to add customer locations (snapped to grid). Press ENTER to start BCO.")

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

        pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
        msg = f"Customers: {len(coords) - 1} | Left-click to add, ENTER to start BCO"
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

    bco_visual(coords)

if __name__ == "__main__":
    main()
