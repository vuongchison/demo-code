from random import randint, shuffle
from time import time_ns

l = list(range(1000000))
shuffle(l)
s = set(range(1000000))

keys = [randint(0, 1000000 - 1) for i in range(1000)]

start_time = time_ns()
for k in keys:
    k in l

end_time = time_ns()
print("check in list: ", (end_time - start_time) / 1000000, "ms")

start_time = time_ns()
for k in keys:
    k in s

end_time = time_ns()
print("check in set: ", (end_time - start_time) / 1000000, "ms")


