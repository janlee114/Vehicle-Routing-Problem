import pygame
import random
import math
import copy

# ------------------------------
# PARAMETERS
# ------------------------------
RING_COUNT = 30
ITERATIONS = 200
STEP = 1                # number of positions partially adopted
THROW_RATE = 0.3        # chance of random throw
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
pygame.display.set_caption("Deliver-All-First Ring Toss Game Optimization (RTGO)")
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
    for i in range(len(full)-1):
        total += math.hypot(coords[full[i]][0]-coords[full[i+1]][0],
                            coords[full[i]][1]-coords[full[i+1]][1])
    return total

def random_route(coords):
    r = list(range(1, len(coords)))
    random.shuffle(r)
    return r

def swap_move(route):
    if len(route) < 2:
        return route[:]
    r = route[:]
    i, j = random.sample(range(len(r)), 2)
    r[i], r[j] = r[j], r[i]
    return r

def toss_ring(agent, target):
    """Partially adopt target positions"""
    new = agent[:]
    for _ in range(STEP):
        i = random.randint(0, len(agent)-1)
        new[i] = target[i]
    # repair permutation
    seen, fixed = set(), []
    for c in new:
        if c not in seen:
            fixed.append(c)
            seen.add(c)
    missing = list(set(agent)-seen)
    fixed.extend(missing)
    return fixed

# ------------------------------
# RTGO OPERATORS
# ------------------------------
def random_throw(agent):
    if random.random() < THROW_RATE:
        return swap_move(agent)
    return agent

def aim_at_best(agent, global_best):
    return toss_ring(agent, global_best)

def rtgo_step(agent, global_best):
    a1 = random_throw(agent)
    a2 = aim_at_best(a1, global_best)
    return a2

# ------------------------------
# VISUALIZATION
# ------------------------------
def draw_solution(route, coords, iteration, best_dist):
    screen.fill(WHITE)
    draw_grid()

    pygame.draw.circle(screen, RED, coords[0], 10)
    screen.blit(font.render("Depot", True, BLACK), (coords[0][0]+10, coords[0][1]-10))

    for i,(x,y) in enumerate(coords[1:], start=1):
        pygame.draw.circle(screen, BLUE, (x,y),6)
        screen.blit(font.render(str(i), True, BLACK), (x+5, y-5))

    full = [0] + route + [0]
    for i in range(len(full)-1):
        pygame.draw.line(screen, GREEN, coords[full[i]], coords[full[i+1]], 3)

    pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE,100))
    txt = f"Iteration: {iteration}   Best Distance: {best_dist:.2f}"
    screen.blit(font.render(txt, True, BLACK), (20, SCREEN_SIZE+30))
    pygame.display.flip()

# ------------------------------
# MAIN RTGO LOOP
# ------------------------------
def rtgo_visual(coords):
    population = [random_route(coords) for _ in range(RING_COUNT)]
    global_best = min(population, key=lambda r: total_distance(r, coords))
    best_dist = total_distance(global_best, coords)
    clock = pygame.time.Clock()

    for iteration in range(ITERATIONS):
        new_population = []
        for agent in population:
            moved = rtgo_step(agent, global_best)
            new_population.append(moved)

        population = new_population
        current_best = min(population, key=lambda r: total_distance(r, coords))
        current_dist = total_distance(current_best, coords)
        if current_dist < best_dist:
            global_best = copy.deepcopy(current_best)
            best_dist = current_dist

        draw_solution(global_best, coords, iteration+1, best_dist)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return

    print("\nFinal route:", [0]+global_best+[0])
    print("Total distance:", best_dist)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                return
        pygame.time.wait(100)

# ------------------------------
# MAIN
# ------------------------------
def main():
    coords = [(SCREEN_SIZE//2, SCREEN_SIZE//2)]
    placing = True

    print("Click to add customers (grid-snapped). Press ENTER to start RTGO.")

    while placing:
        screen.fill(WHITE)
        draw_grid()

        pygame.draw.circle(screen, RED, coords[0],10)
        screen.blit(font.render("Depot", True, BLACK), (coords[0][0]+10, coords[0][1]-10))

        for i,(x,y) in enumerate(coords[1:], start=1):
            pygame.draw.circle(screen, BLUE, (x,y),6)
            screen.blit(font.render(str(i), True, BLACK), (x+5, y-5))

        pygame.draw.rect(screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE,100))
        msg = f"Customers: {len(coords)-1} | ENTER to start RTGO"
        screen.blit(font.render(msg, True, BLACK), (20, SCREEN_SIZE+30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                return
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                x,y = event.pos
                if y<SCREEN_SIZE:
                    coords.append(snap_to_grid(x,y))
            if event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN:
                placing=False

    rtgo_visual(coords)

if __name__ == "__main__":
    main()
