import time
from opensimplex import OpenSimplex

gen = OpenSimplex(seed=123)

start = time.time()

for i in range(10000):
    for x in range(100):
        gen.noise2((x+i) / 10.0, 0)

print(time.time() - start)