

n = 5
A = [0] * n

def backtrack(i):
    global n, A
    if i == n:
        print(A)
        return
    
    for value in (0, 1):
        A[i] = value
        backtrack(i + 1)

backtrack(0)
