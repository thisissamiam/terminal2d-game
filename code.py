from opensimplex import OpenSimplex

a = OpenSimplex(seed=123)
b = OpenSimplex(seed=123 + 2**64)

print(a.noise2(1.5, 2.5))
print(b.noise2(1.5, 2.5))