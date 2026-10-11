import pygame
import random
import math

# ------------------------------
# PARAMETERS
# ------------------------------
POP_SIZE = 20
ITERATIONS = 100
SEGMENT_LENGTH = 4  # partial segment size for recombination
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
pygame.display.set_caption("Deliver-All-First POPMUSIC Algorithm")
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

def create_random_route(coords):
    route = list(range(1, len(coords)))
    random.shuffle(route)
    return route

def two_opt(route, coords):
    best = route
    improved = True
    while improved:
        improved = False
        best_dist = total_distance(best, coords)
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best)):
                new_route = best[:i] + best[i:j][::-1] + best[j:]
                if total_distance(new_route, coords) < best_dist:
                    best = new_route
                    improved = True
                    break
            if improved:
                break
    return best

def recombine_segments(parents, coords):
    """Combine good partial segments from top parent routes"""
    all_segments = []
    for p in parents:
        for i in range(0, len(p), SEGMENT_LENGTH):
            segment = p[i:i+SEGMENT_LENGTH]
            if segment:
                all_segments.append(segment)
    random.shuffle(all_segments)

    combined = []
    seen = set()
    for seg in all_segments:
        for node in seg:
            if node not in seen:
                combined.append(node)
                seen.add(node)
    missing = set(range(1, len(coords))) - seen
    combined.extend(list(missing))
    return combined

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
    for i in range(len(full_route) - 1):
        pygame.draw.line(screen, GREEN, coords[full_route[i]], coords[full_route[i + 1]], 3)

    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
    text = f"Iteration: {iteration}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(text, True, BLACK), (20, SCREEN_SIZE + 30))
    pygame.display.flip()

# ------------------------------
# POPMUSIC MAIN LOOP
# ------------------------------
def popmusic_visual(coords):
    population = [create_random_route(coords) for _ in range(POP_SIZE)]
    population = [two_opt(r, coords) for r in population]
    best_route = min(population, key=lambda r: total_distance(r, coords))
    best_dist = total_distance(best_route, coords)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        # Select top routes for recombination
        population.sort(key=lambda r: total_distance(r, coords))
        top_parents = population[:POP_SIZE // 3]

        # Recombine partial segments
        new_route = recombine_segments(top_parents, coords)

        # Local optimization
        new_route = two_opt(new_route, coords)

        # Replace worst if improved
        if total_distance(new_route, coords) < total_distance(population[-1], coords):
            population[-1] = new_route

        # Update best
        current_best = min(population, key=lambda r: total_distance(r, coords))
        current_dist = total_distance(current_best, coords)
        if current_dist < best_dist:
            best_route = current_best
            best_dist = current_dist

        draw_solution(best_route, coords, iteration + 1, best_dist)
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
    coords = [(SCREEN_SIZE // 2, SCREEN_SIZE // 2)]  # depot
    placing = True

    print("Click to add customer locations (snapped to grid). Press ENTER to start POPMUSIC.")

    while placing:
        screen.fill(WHITE)
        draw_grid()

        # Draw depot
        pygame.draw.circle(screen, RED, coords[0], 10)
        screen.blit(font.render("Depot", True, BLACK), (coords[0][0] + 10, coords[0][1] - 10))

        # Draw points
        for i, (x, y) in enumerate(coords[1:], start=1):
            pygame.draw.circle(screen, BLUE, (x, y), 6)
            screen.blit(font.render(str(i), True, BLACK), (x + 5, y - 5))

        pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
        msg = f"Customers: {len(coords) - 1} | Left-click to add, ENTER to start POPMUSIC"
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

    popmusic_visual(coords)

if __name__ == "__main__":
    main()
