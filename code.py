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
            chunk[y * width + x] = '#`255,0,255`'
    # for textx in range(len(str(i))):
    #     chunk[1-height * width + textx] = str(i)[textx]
    frame = ''
    for i in range(len(chunk) // width):
        for tile in chunk[i*width:i*width+width]:
            for char in tile: # Loop everything inside of the tile to find the color seperator
                incolorcode = False
                if char == '`': # If the char is the color seperator
                    if incolorcode:
                        incolorcode = False # This would trigger at the end of 255,0,255, meaning to that is the end, and the next tile is coming up so inside of color should go to false.
                    else:
                        incolorcode = True # For example if not inside of 255,0,255 yet, set inside to true.
                        colorcode # Reset color code because the color code mode was just entered.
                        continue
                if incolorcode:
                    colorcode += char # Add to color code the next char
    #     frame = frame + '\n' + "".join(line)
    # print(term.home + term.color_rgb(255, 0, 255)(frame), end="", flush=True)
    # time.sleep(1)