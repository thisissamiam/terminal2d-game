from opensimplex import OpenSimplex

a = OpenSimplex(seed=123)
b = OpenSimplex(seed=123 + 2**64)

print(a.noise2(1.5, 2.5))
print(b.noise2(1.5, 2.5))from opensimplex import OpenSimplex

width = 100
height = 30

def generateworld(seed):
    gen = OpenSimplex(seed=seed)
    world = []

    for y in range(height):
        for x in range(width):
            world.append(gen.noise2(x / 10.0, y / 10.0))

    return world


seed = 123456789
original = generateworld(seed)

def identical(difference):
    return original == generateworld(seed + difference)


# Exponential search
low = 0
high = 1

while not identical(high):
    low = high
    high *= 2
    print('Searching:', high)

print('Collision found at:', high)

# Binary search
while high - low > 1:
    middle = (low + high) // 2

    if identical(middle):
        high = middle
    else:
        low = middle

print('\nSmallest collision found:', high)
print('Second seed:', seed + high)