import random
from opensimplex import OpenSimplex
import blessed
world = [] # Create the 2d world, starting as nothing
seed = random.randint(0, 100000000) # Generate the seed, determines what is generated
gen = OpenSimplex(seed=seed)
term = blessed.Terminal() # Term is basicly the terminal, allows editing and getting data about the terminal.
print(term.clear) # Clear the screen before printing
# Chunk Settings
width = 100
height = 30
chunk = [' '] * width * height
for x in range(width):
    isflat = abs(int(gen.noise2(x / 20.0, 0))) < 0.2
    if isflat:
        topheight = lasttopheight
    else:
        topheight = 15 - int(gen.noise2(x / 10.0, 0) * 10)
    for y in range(topheight, 30):
        chunk[y * width + x] = '!'
    lasttopheight = topheight


print(term.home, end="")
for i in range(len(chunk) // width):
    print(term.color_rgb(255, 0, 255)("".join(chunk[i*width:i*width+width])))