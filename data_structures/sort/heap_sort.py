# A = [5, 4, 2, 2, 6, 7, 1, 8, 9]
# n = len(A)
from time import time_ns
import heapq

n = int(input())
A = [int(e) for e in input().split(',') if e]


start = time_ns()

H = A[:]
heapq.heapify(H)
for i in range(n):
    A[i] = heapq.heappop(H)

end = time_ns()

print(A[:20])
print("run in: ", (end - start) / 1000000, "ms")