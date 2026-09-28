import random
from opensimplex import OpenSimplex
import blessed
import time
world = [] # Create the 2d world, starting as nothing
seed = random.randint(0, 100000000) # Generate the seed, determines what is generated
gen = OpenSimplex(seed=seed)
term = blessed.Terminal() # Term is basicly the terminal, allows editing and getting data about the terminal.
print(term.clear) # Clear the screen before printing
# Chunk Settings
width = 100
height = 30
for i in range(10000):
    chunk = [' '] * width * height # Reset current chunk data before calculating terrain
    for x in range(width):
        topheight = 15 - int(gen.noise2((x+i) / 10.0, 0) * 10)
        for y in range(topheight, 30):
            chunk[y * width + x] = '█'
            time.sleep(1)


    frame = ''
    for i in range(len(chunk) // width):
        frame = frame + '\n' + "".join(chunk[i*width:i*width+width])
        time.sleep(1)
    print(term.home + term.color_rgb(255, 0, 255)(frame), end="", flush=True)
    time.sleep(1)