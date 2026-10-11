import pygame
import random
import math

# ------------------------------
# PARAMETERS
# ------------------------------
POP_SIZE = 50
GENERATIONS = 300
MUTATION_RATE = 0.1
SCREEN_SIZE = 700
GRID_SPACING = 50  # snap interval

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
pygame.display.set_caption("Deliver-All-First GA")
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
# GA UTILS
# ------------------------------
def create_individual(coords):
    """Random sequence of all customers"""
    customers = list(range(1, len(coords)))
    random.shuffle(customers)
    return customers

def repair_individual(individual, coords):
    """Ensure all customers are visited exactly once"""
    all_customers = set(range(1, len(coords)))
    missing = all_customers - set(individual)
    individual = [c for c in individual if c in all_customers]
    individual += list(missing)
    return individual

def total_distance(individual, coords):
    total = 0
    route = [0] + individual + [0]  # start and end at depot
    for i in range(len(route)-1):
        total += math.hypot(coords[route[i]][0]-coords[route[i+1]][0],
                            coords[route[i]][1]-coords[route[i+1]][1])
    return total

def crossover(p1, p2):
    """Order crossover"""
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))
    child = [None]*size
    child[a:b] = p1[a:b]
    fill_pos = b
    for gene in p2:
        if gene not in child:
            if fill_pos >= size:
                fill_pos = 0
            child[fill_pos] = gene
            fill_pos += 1
    return child

def mutate(ind):
    ind = ind[:]
    for i in range(len(ind)):
        if random.random() < MUTATION_RATE:
            j = random.randint(0, len(ind)-1)
            ind[i], ind[j] = ind[j], ind[i]
    return ind

def tournament_selection(pop, coords, k=3):
    return min(random.sample(pop, k), key=lambda ind: total_distance(ind, coords))

# ------------------------------
# PYGAME VISUALIZATION
# ------------------------------
def draw_solution(best, coords, gen, best_dist):
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
    route = [0] + best + [0]
    for i in range(len(route)-1):
        pygame.draw.line(screen, GREEN, coords[route[i]], coords[route[i+1]], 3)

    # Info panel
    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, 100))
    text = f"Generation: {gen}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(text, True, BLACK), (20, SCREEN_SIZE+30))
    pygame.display.flip()

# ------------------------------
# GA MAIN LOOP
# ------------------------------
def genetic_algorithm_visual(coords):
    pop = [create_individual(coords) for _ in range(POP_SIZE)]
    best = min(pop, key=lambda ind: total_distance(ind, coords))
    clock = pygame.time.Clock()
    gen = 0
    running = True

    while running and gen < GENERATIONS:
        gen += 1
        new_pop = []
        for _ in range(POP_SIZE):
            p1 = tournament_selection(pop, coords)
            p2 = tournament_selection(pop, coords)
            child = crossover(p1, p2)
            child = mutate(child)
            child = repair_individual(child, coords)
            new_pop.append(child)
        pop = new_pop
        gen_best = min(pop, key=lambda ind: total_distance(ind, coords))
        if total_distance(gen_best, coords) < total_distance(best, coords):
            best = gen_best

        draw_solution(best, coords, gen, total_distance(best, coords))
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    print("\nFinal route:", [0]+best+[0])
    print("Total distance:", total_distance(best, coords))

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

    print("Click to add customer locations (snapped to grid). Press ENTER to start GA.")

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
        msg = f"Customers: {len(coords)-1} | Left-click to add, ENTER to start GA"
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

    genetic_algorithm_visual(coords)

if __name__ == "__main__":
    main()
