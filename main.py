from opensimplex import OpenSimplex
import random
import time
import os
world = []

seed = random.randint(0, 100000000)
print("Seed:", seed)
l = 0
gen = OpenSimplex(seed=seed)
for i in range(1000):

	def loop():
	    global l
	    global world

	    width = 100
	    height = 30

	    world = []

	    for y in range(height):
	        row = []
	        for x in range(width):
	            row.append(' ')
	        world.append(row)

	    for x in range(width):
	        small = gen.noise2((x + l) / 10.0, 0) * 2
medium = gen.noise2((x + l) / 50.0, 0) * 4
big = gen.noise2((x + l) / 200.0, 0) * 8

terrain_height = int(8 + small + medium + big)

	        for y in range(terrain_height):
	            world[height - 1 - y][x] = 'D'

	loop()

	for row in world:
	    print("".join(row))
	l += 1
	time.sleep(1/60)
	os.system('clear')
