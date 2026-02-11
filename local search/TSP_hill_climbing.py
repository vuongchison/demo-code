import random
import math
import matplotlib.pyplot as plt

# -------- Problem --------
N = 100
CITIES = list(range(N))

# Generate random 2D points (x, y)
POINTS = [(random.randint(0, 500), random.randint(0, 500)) for _ in range(N)]

# Calculate Euclidean distance matrix
DIST = [[0.0]*N for _ in range(N)]
for i in range(N):
    for j in range(i+1, N):
        x1, y1 = POINTS[i]
        x2, y2 = POINTS[j]
        d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        DIST[i][j] = DIST[j][i] = d

def tour_length(tour):
    return sum(DIST[tour[i]][tour[i+1]] for i in range(len(tour)-1)) \
           + DIST[tour[-1]][tour[0]]

def plot_tour(tour, points):
    x = [points[i][0] for i in tour] + [points[tour[0]][0]]
    y = [points[i][1] for i in tour] + [points[tour[0]][1]]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'o-', mfc='r', markersize=8)
    plt.title(f"Best Tour (Length: {tour_length(tour):.2f})")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    
    for i, (px, py) in enumerate(points):
        plt.annotate(str(i), (px, py), textcoords="offset points", xytext=(0,5), ha='center')
        
    plt.grid(True)
    plt.show()

def init_tour():
    tour = list(range(N))
    random.shuffle(tour)
    return tour

def best_neighbor_swap(tour):
    best_neighbor = None
    best_length = float('inf')
    for i in range(N - 1):
        for j in range(i + 1, N):
            new_tour = tour[:]
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            new_tour_length = tour_length(new_tour)
            if new_tour_length < best_length:
                best_neighbor = new_tour
    return best_neighbor, best_length



def best_neighbor_2_opt(tour):
    best_neighbor = None
    best_length = float('inf')
    curr_tour_length = tour_length(tour)
    for i in range(N - 1):
        A = tour[i]
        B = tour[i + 1]
        for j in range(i + 2, N):
            C = tour[j]
            D = tour[(j + 1) % N]
            delta = (DIST[A][C] + DIST[B][D]) - (DIST[A][B] + DIST[C][D])
            if delta < 0:
                new_tour_len = curr_tour_length + delta
                if new_tour_len < best_length:
                    best_length = new_tour_len
                    best_neighbor = tour[:]
                    best_neighbor[i + 1 : j + 1] = reversed(best_neighbor[i + 1 : j + 1])
    return best_neighbor, best_length

def hill_climbing(current_tour):
    current_tour_length = tour_length(current_tour)
    while True:
        best_neighbor, best_neighbor_length = best_neighbor_2_opt(current_tour)
        if best_neighbor_length >= current_tour_length:
            return current_tour, current_tour_length
        current_tour = best_neighbor
        current_tour_length = best_neighbor_length
        

if __name__ == "__main__":

    best_tour, best_len = hill_climbing(init_tour())

    print("Best tour:", best_tour)
    print("Best length:", best_len)
    plot_tour(best_tour, POINTS)



