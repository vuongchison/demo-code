import random
import math
import matplotlib.pyplot as plt
from collections import defaultdict


# ==================
#Problem
N = 10
CAPACITY = 4
MAX_RIDE = 60
# ===================

LOCATIONS = [f"R{i}" for i in range(N)] + [f"C{i}" for i in range(N)]


# Generate random 2D points (x, y)
POINTS = [(random.randint(0, 50), random.randint(0, 50)) for _ in range(2 * N)]
NAME_POINTS = {LOCATIONS[i]: POINTS[i] for i in range(2 * N)}

# Calculate Euclidean distance matrix
DIST = defaultdict(dict)
for i in range(2 * N):
    for j in range(i+1, 2 * N):
        x1, y1 = POINTS[i]
        x2, y2 = POINTS[j]
        d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        DIST[LOCATIONS[i]][LOCATIONS[j]] = DIST[LOCATIONS[j]][LOCATIONS[i]] = d

# print(DIST)

def plot_tour(tour):
    x = [NAME_POINTS[i][0] for i in tour]
    y = [NAME_POINTS[i][1] for i in tour]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'o-', mfc='r', markersize=8)
    plt.title(f"Best Tour (Length: {tour_length(tour):.2f})")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    
    for i, (px, py) in enumerate(POINTS):
        plt.annotate(LOCATIONS[i], (px, py), textcoords="offset points", xytext=(0,5), ha='center')
        
    plt.grid(True)
    plt.show()

# ================================================

def tour_length(tour):
    return sum(DIST[tour[i]][tour[i+1]] for i in range(len(tour)-1))

def precedence_violation(tour):
    # Restaurant before Client constraint violation
    pos = {tour[i] : i for i in range(2 * N)}
    count = 0
    for p in range(N):
        r = pos[f'R{p}']
        c = pos[f'C{p}']
        if c < r:
            count += 1
    return count

def capacity_violation(tour):
    load = 0
    max_load = 0
    for loc in tour:
        if loc.startswith('R'):
            load += 1
        else:
            load -= 1
        if load > max_load:
            max_load = load
    if max_load <= CAPACITY:
        return 0
    else:
        return max_load - CAPACITY


def cold_violation(tour):
    total_viol = 0
    pos = {tour[i] : i for i in range(2 * N)}
    for p in range(N):
        r = pos[f'R{p}']
        c = pos[f'C{p}']
        shipping_dist = 0
        for i in range(r, c):
            shipping_dist += DIST[tour[i]][tour[i+1]]
        if shipping_dist > MAX_RIDE:
            total_viol += (shipping_dist - MAX_RIDE)
    return total_viol


def is_feasible(tour):
    return (precedence_violation(tour) == 0) and (capacity_violation(tour) == 0) and (cold_violation(tour) == 0)

# ---------------- GLS components ----------------
lambda1, lambda2, lambda3 = 50.0, 50.0, 10.0


def F(tour):
    return tour_length(tour) + lambda1 * precedence_violation(tour) + lambda2 * capacity_violation(tour) + lambda3 * cold_violation(tour)

def neighbor(tour):
    neighbor = tour[:]
    i, j = random.sample(range(2 * N), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def update_penalties(tour):
    global lambda1, lambda2, lambda3
    #update lambda1, lambda2, lambda3
    if precedence_violation(tour) == 0:
        lambda1 *= 0.98
    else:
        lambda1 *= 1.1

    if capacity_violation(tour) == 0:
        lambda2 *= 0.98
    else:
        lambda2 *= 1.1

    if cold_violation(tour) == 0:
        lambda3 *= 0.98
    else:
        lambda3 *= 1.1

def init_tour():
    tour = LOCATIONS[:]
    random.shuffle(tour)
    return tour

# ---------------- Main GLS loop ----------------
def guided_local_search(max_iter=10000):
    #return a feasible tour
    #if can't, return None
    best, best_len = None, float('inf')
    current_tour = init_tour()
    for _ in range(max_iter):
        neighbor_tour = neighbor(current_tour)
        if F(neighbor_tour) <= F(current_tour):
            current_tour = neighbor_tour
        update_penalties(current_tour)
        current_tour_len = tour_length(current_tour)
        if is_feasible(current_tour) and current_tour_len < best_len:
            best = current_tour
            best_len = current_tour_len
            print("Best tour:", best)
            print("Best length:", best_len)
        
        if _ % 100 == 0:
            print("Current len:", current_tour_len, "| precedence_violation:", precedence_violation(current_tour), "| capacity_violation:", capacity_violation(current_tour), "| cold_violation:", cold_violation(current_tour))
            print("lambda1:", lambda1, "| lambda2:", lambda2, "| lambda3:", lambda3)

    return best, best_len

if __name__ == "__main__":
    best_tour, best_length = min((guided_local_search() for _ in range(10)), key=lambda t: t[1])
    # best_tour, best_length = guided_local_search()
    # best_tour = init_tour()
    print("Best tour:", best_tour)
    print("Best length:", best_length)
    if best_tour:
        plot_tour(best_tour)

