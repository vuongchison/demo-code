import random
import time

# ===============================
# Problem Definition
# ===============================
values = []
weights = []
W = 0
n = 0

def read_data():
    global values, weights, W, n
    n = int(input())
    values = [int(x) for x in input().split()]
    weights = [int(x) for x in input().split()]
    W = int(input())

# ===============================
# GA Parameters
# ===============================

POP_SIZE = 80
GENERATIONS = 100
PC = 0.8        # crossover probability
PM = 0.02       # mutation probability
ELITE = 2       # number of elite individuals

# ===============================
# Fitness + Repair
# ===============================

def repair(chrom):
    """Remove items randomly until feasible."""
    while total_weight(chrom) > W:
        ones = [i for i in range(n) if chrom[i] == 1]
        if not ones:
            break
        idx = random.choice(ones)
        chrom[idx] = 0
    return chrom


def total_weight(chrom):
    return sum(w for w, g in zip(weights, chrom) if g)


def total_value(chrom):
    return sum(v for v, g in zip(values, chrom) if g)


def fitness(chrom):
    return total_value(chrom)


# ===============================
# Initialization
# ===============================

def random_chrom():
    chrom = [random.randint(0, 1) for _ in range(n)]
    return repair(chrom)


# ===============================
# Selection
# ===============================

def select(pop, k=3):
    candidates = random.sample(pop, k)
    return max(candidates, key=fitness)

# ===============================
# Crossover
# ===============================

def crossover(p1, p2):
    if random.random() > PC:
        return p1[:], p2[:]

    point = random.randint(1, n - 1)
    c1 = p1[:point] + p2[point:]
    c2 = p2[:point] + p1[point:]
    return c1, c2

# ===============================
# Mutation
# ===============================

def mutate(chrom):
    for i in range(n):
        if random.random() < PM:
            chrom[i] ^= 1



# ===============================
# GA Main Loop
# ===============================
def main_loop():

    best = None
    best_value = 0
    population = [random_chrom() for _ in range(POP_SIZE)]

    for gen in range(GENERATIONS):

        new_population = []

        # Elitism
        sorted_pop = sorted(population, key=fitness, reverse=True)
        elites = sorted_pop[:ELITE]
        new_population.extend(elites)

        while len(new_population) < POP_SIZE:
            p1 = select(population)
            p2 = select(population)

            c1, c2 = crossover(p1, p2)
            mutate(c1)
            mutate(c2)

            repair(c1)
            repair(c2)

            new_population.extend([c1, c2])

        population = new_population[:POP_SIZE]

        current_best = max(population, key=fitness)
        current_best_value = fitness(current_best)
        if best is None or current_best_value > best_value:
            best = current_best
            best_value = current_best_value
            print("New best: ", best_value)

        if gen % 50 == 0:
            print(f"Gen {gen} | Best value = {fitness(best)}")
    return best

if __name__ == "__main__":
    read_data()
    t = time.time()
    best = main_loop()
    print("solve in:", time.time() - t, "s")

    print("\nBest solution:", best)
    print("Total value :", total_value(best))
    print("Total weight:", total_weight(best))