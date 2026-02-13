import random
import math

# -----------------------
# Parameters
# -----------------------
N_CUSTOMERS = 100        # number of customers (excluding depot)
MAX_COORD = 500
MAX_DEMAND = 3
CAPACITY = 30
SEED = 42

random.seed(SEED)

# -----------------------
# Generate Points
# -----------------------

# Depot at index 0 (centered for nicer visualization)
POINTS = [(250, 250)]

# Customers 1..N
for _ in range(N_CUSTOMERS):
    x = random.randint(0, MAX_COORD)
    y = random.randint(0, MAX_COORD)
    POINTS.append((x, y))

N = N_CUSTOMERS + 1   # include depot

# -----------------------
# Generate Demands
# -----------------------

DEMAND = [0]  # depot demand = 0

for _ in range(N_CUSTOMERS):
    DEMAND.append(random.randint(1, MAX_DEMAND))

# -----------------------
# Distance Matrix
# -----------------------

DIST = [[0.0]*N for _ in range(N)]

for i in range(N):
    for j in range(i+1, N):
        x1, y1 = POINTS[i]
        x2, y2 = POINTS[j]
        d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        DIST[i][j] = DIST[j][i] = d

# -----------------------
# Print Output
# -----------------------

print(N)
# print(K)
print(CAPACITY)

# print("\nPOINTS (index x y):")
for (x, y) in POINTS:
    print(x, y)

# print("\nDEMAND:")
print(*DEMAND)

# print("\nDISTANCE MATRIX:")
for i in range(N):
    print(*DIST[i])