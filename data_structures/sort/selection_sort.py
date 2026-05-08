# A = [5, 4, 2, 2, 6, 7, 1, 8, 9]
# n = len(A)
from time import time_ns

n = int(input())
A = [int(e) for e in input().split(',') if e]

start = time_ns()
for i in range(n):

    min_val = float('inf')
    min_index = i

    for j in range(i, n):
        if A[j] < min_val:
            min_val = A[j]
            min_index = j

    A[i], A[min_index] = A[min_index], A[i]

end = time_ns()

print(A[:20])
print("run in: ", (end - start) / 1000000, "ms")