import pygame
import random
import math
import copy

# ------------------------------
# PARAMETERS
# ------------------------------
FISH_COUNT = 30
ITERATIONS = 200
VISUAL = 3          # visual range (# of neighbors checked)
STEP = 1            # movement step
TRY_NUMBER = 5      # attempts per behavior
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
pygame.display.set_caption("Deliver-All-First Artificial Fish Swarm Algorithm")
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
# ROUTE OPERATIONS
# ------------------------------
def total_distance(route, coords):
    total = 0
    full_route = [0] + route + [0]
    for i in range(len(full_route)-1):
        total += math.hypot(coords[full_route[i]][0] - coords[full_route[i+1]][0],
                            coords[full_route[i]][1] - coords[full_route[i+1]][1])
    return total

def random_route(coords):
    route = list(range(1, len(coords)))
    random.shuffle(route)
    return route

def swap_move(route):
    """Perform a small random swap (local change)."""
    new_route = route[:]
    a, b = random.sample(range(len(route)), 2)
    new_route[a], new_route[b] = new_route[b], new_route[a]
    return new_route

# ------------------------------
# AFSA FUNCTIONS
# ------------------------------
def prey(fish, coords):
    """Random exploration (prey behavior)."""
    best = fish
    best_dist = total_distance(fish, coords)
    for _ in range(TRY_NUMBER):
        candidate = swap_move(fish)
        cand_dist = total_distance(candidate, coords)
        if cand_dist < best_dist:
            best = candidate
            best_dist = cand_dist
    return best

def swarm(fish, school, coords):
    """Swarm behavior — move toward the best neighbor (within visual range)."""
    neighbors = random.sample(school, min(VISUAL, len(school)))
    best_neighbor = min(neighbors, key=lambda f: total_distance(f, coords))
    if total_distance(best_neighbor, coords) < total_distance(fish, coords):
        new_fish = follow(fish, best_neighbor)
        return new_fish
    else:
        return prey(fish, coords)

def follow(fish, best_neighbor):
    """Follow behavior — partially adopt the neighbor’s structure."""
    new_fish = fish[:]
    # partially copy positions from best neighbor
    for _ in range(STEP):
        i = random.randint(0, len(fish) - 1)
        new_fish[i] = best_neighbor[i]
    # remove duplicates and reinsert missing nodes
    seen, fixed = set(), []
    for c in new_fish:
        if c not in seen:
            fixed.append(c)
            seen.add(c)
    missing = list(set(fish) - seen)
    fixed += missing
    return fixed

def move_random(fish):
    """Random movement (when no better state found)."""
    return swap_move(fish)

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

    # Route
    full_route = [0] + route + [0]
    for i in range(len(full_route)-1):
        pygame.draw.line(screen, GREEN, coords[full_route[i]], coords[full_route[i+1]], 3)

    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
    text = f"Iteration: {iteration}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(text, True, BLACK), (20, SCREEN_SIZE + 30))
    pygame.display.flip()

# ------------------------------
# AFSA MAIN LOOP
# ------------------------------
def afsa_visual(coords):
    school = [random_route(coords) for _ in range(FISH_COUNT)]
    best_fish = min(school, key=lambda f: total_distance(f, coords))
    best_dist = total_distance(best_fish, coords)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        new_school = []
        for fish in school:
            new_fish = swarm(fish, school, coords)
            new_school.append(new_fish)

        school = new_school
        current_best = min(school, key=lambda f: total_distance(f, coords))
        current_dist = total_distance(current_best, coords)

        if current_dist < best_dist:
            best_fish = copy.deepcopy(current_best)
            best_dist = current_dist

        draw_solution(best_fish, coords, iteration+1, best_dist)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    print("\nFinal route:", [0] + best_fish + [0])
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

    print("Click to add customer locations (snapped to grid). Press ENTER to start AFSA.")

    while placing:
        screen.fill(WHITE)
        draw_grid()

        # Draw depot
        pygame.draw.circle(screen, RED, coords[0], 10)
        screen.blit(font.render("Depot", True, BLACK), (coords[0][0]+10, coords[0][1]-10))

        # Draw customers
        for i, (x, y) in enumerate(coords[1:], start=1):
            pygame.draw.circle(screen, BLUE, (x, y), 6)
            screen.blit(font.render(str(i), True, BLACK), (x+5, y-5))

        pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
        msg = f"Customers: {len(coords)-1} | Left-click to add, ENTER to start AFSA"
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

    afsa_visual(coords)

if __name__ == "__main__":
    main()
