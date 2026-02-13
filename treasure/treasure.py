from copy import copy
import time

n = int(input())
v = [int(x) for x in input().split()]
w = [int(x) for x in input().split()]
b = int(input())

#solve here
#run test: python treasure.py < tc1.txt

best_sol = [None] * n
best_value = float('-inf')

choose = [0] * n
v_curr = 0
w_curr = 0

def upper_bound(i):
    v_est = v_curr
    slot = b - w_curr
    for j in range(i + 1, n):
        if slot >= w[j]:
            v_est += v[j]
            slot -= w[j]
        else:
            v_est += slot/w[j] * v[j]
    return v_est

def sort_items():
    t = []
    for i in range(n):
        t.append((v[i], w[i]))
    
    t.sort(key=lambda a: a[0]/a[1], reverse=True)

    for i in range(n):
        v[i], w[i] = t[i]

def backtrack(i):
    global best_sol, best_value, w_curr, v_curr
    if i == n:
        if v_curr > best_value:
            best_sol = copy(choose)
            best_value = v_curr
            print("new best:", best_value)
        return
    
    for value in (0, 1):
        choose[i] = value
        if value == 1:
            v_curr += v[i]
            w_curr += w[i]
        if w_curr <= b and upper_bound(i) > best_value:
            backtrack(i + 1)
        if value == 1:
            v_curr -= v[i]
            w_curr -= w[i]

print("Solving...")
t = time.time()
sort_items()
backtrack(0)
print("Solve in:", time.time() - t, "s")
print(best_sol)
print(best_value)