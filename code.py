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
for y in range(height): # Make a chunk
        chunk = []
        for i in range(3000):
            chunk.append('*')
        
print(term.home() + term.color_rgb(255, 0, 255)("".join(chunk)))