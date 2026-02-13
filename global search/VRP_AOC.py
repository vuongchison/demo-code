import random
import matplotlib.pyplot as plt

N = 0
CAPACITY = 0
POINTS = []
DEMAND = []
DIST = []

def read_data():
    global N, CAPACITY, POINTS, DEMAND, DIST

    N = int(input())              # number of nodes (including depot)
    CAPACITY = int(input())

    # Read coordinates
    POINTS = []
    for _ in range(N):
        x, y = map(float, input().split())
        POINTS.append((x, y))

    # Read demand
    DEMAND = list(map(int, input().split()))

    # Read distance matrix
    DIST = []
    for _ in range(N):
        row = list(map(float, input().split()))
        DIST.append(row)

def visualize_solution(solution):
    global POINTS, DEMAND
    plt.figure(figsize=(8, 8))

    xs = [p[0] for p in POINTS]
    ys = [p[1] for p in POINTS]

    # Plot nodes
    plt.scatter(xs[1:], ys[1:], c='blue')
    plt.scatter(xs[0], ys[0], c='red', marker='s', s=120, label="Depot")

    # Labels
    for i, (x, y) in enumerate(POINTS):
        if i == 0:
            plt.text(x, y, "Depot", fontsize=10, ha='right')
        else:
            plt.text(x, y, f"{i}({DEMAND[i]})",
                     fontsize=9, ha='right')

    # New colormap API
    cmap = plt.colormaps.get_cmap('tab20')
    num_routes = len(solution)

    for r_idx, route in enumerate(solution):
        route_x = [POINTS[i][0] for i in route]
        route_y = [POINTS[i][1] for i in route]

        color = cmap(r_idx % cmap.N)

        plt.plot(route_x, route_y,
                 color=color,
                 linewidth=2,
                 label=f"Route {r_idx+1}")

    plt.title("CVRP Solution")
    plt.legend()
    plt.grid(True)
    plt.show()

def two_opt_route(route, DIST):
    """
    route: [0, i1, i2, ..., ik, 0]
    DIST: distance matrix
    """

    improved = True
    n = len(route)

    while improved:
        improved = False

        # skip depot at index 0 and last index
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):

                A, B = route[i - 1], route[i]
                C, D = route[j], route[j + 1]

                delta = (
                    DIST[A][C] + DIST[B][D]
                    - DIST[A][B] - DIST[C][D]
                )

                if delta < -1e-9:
                    # Reverse segment
                    route[i:j + 1] = reversed(route[i:j + 1])
                    improved = True

        # continue until no improvement

    return route

def local_search(solution, DIST):
    improved_solution = []

    for route in solution:
        if len(route) > 4:   # at least 2 customers
            route = two_opt_route(route, DIST)
        improved_solution.append(route)

    return improved_solution

class ACO_VRP:
    def __init__(self, dist, demand, capacity,
                 n_ants=20, n_iter=100,
                 alpha=1.0, beta=2.0,
                 rho=0.1):

        self.dist = dist
        self.demand = demand
        self.capacity = capacity
        self.n = len(dist) - 1  # number of customers
        self.n_ants = n_ants
        self.n_iter = n_iter
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        self.init_pheromone()

    def init_pheromone(self):
        # Initialize pheromone
        self.tau = [[1.0 for _ in range(self.n + 1)]
                    for _ in range(self.n + 1)]
        self.global_best = None
        self.global_best_cost = float("inf")

    # ----------------------------
    # Construct solution for 1 ant
    # ----------------------------
    def construct_solution(self):

        unvisited = set(range(1, self.n + 1))
        solution = []

        while unvisited:

            route = [0]
            remaining = self.capacity
            current = 0

            while True:

                # Feasible customers
                feasible = [j for j in unvisited
                            if self.demand[j] <= remaining]

                if not feasible:
                    break

                # Compute probabilities
                scores = []
                for j in feasible:
                    tau = self.tau[current][j] ** self.alpha
                    eta = (1.0 / self.dist[current][j]) ** self.beta
                    scores.append(tau * eta)

                total = sum(scores)
                probs = [s / total for s in scores]

                # Roulette wheel selection
                r = random.random()
                cumulative = 0.0
                for j, p in zip(feasible, probs):
                    cumulative += p
                    if r <= cumulative:
                        next_customer = j
                        break

                route.append(next_customer)
                remaining -= self.demand[next_customer]
                unvisited.remove(next_customer)
                current = next_customer

            route.append(0)
            solution.append(route)

        return solution

    # ----------------------------
    # Evaluate solution
    # ----------------------------
    def evaluate(self, solution):
        total = 0
        for route in solution:
            for i in range(len(route) - 1):
                total += self.dist[route[i]][route[i + 1]]
        return total

    # ----------------------------
    # Pheromone update
    # ----------------------------
    def update_pheromone(self):

        # Evaporation
        for i in range(self.n + 1):
            for j in range(self.n + 1):
                self.tau[i][j] *= (1 - self.rho)

        # Reinforce global best
        for route in self.global_best:
            for i in range(len(route) - 1):
                a = route[i]
                b = route[i + 1]
                self.tau[a][b] += 1.0 / self.global_best_cost

    # ----------------------------
    # Main loop
    # ----------------------------
    def run(self):

        for it in range(self.n_iter):

            for _ in range(self.n_ants):

                solution = self.construct_solution()
                solution = local_search(solution, self.dist)
                cost = self.evaluate(solution)

                if cost < self.global_best_cost:
                    self.global_best = solution
                    self.global_best_cost = cost
                    print(f"it {it}, New best:", self.global_best_cost)

            self.update_pheromone()

        return self.global_best, self.global_best_cost

if __name__ == "__main__":
    read_data()

    aco = ACO_VRP(DIST, DEMAND, CAPACITY,
                # n_ants=50, n_iter=100) for n=50
                n_ants=70, n_iter=150) #for n=100

    best_solution, best_cost = aco.run()

    print("Best solution:", best_solution)
    print("Best cost:", best_cost)
    visualize_solution(best_solution)