import random
import math

N = 20
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

print(N)
print('\n'.join(f'{point[0]} {point[1]}' for point in POINTS))
for i in range(N):
    print(*DIST[i], sep=' ')
