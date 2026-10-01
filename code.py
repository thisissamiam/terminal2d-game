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
            chunk[y * width + x] = '#`100,0,255`'
    for textx in range(len(str(i))): # Shows X POS on the screen
        chunk[1-height * width + textx] = str(i)[textx]
    frame = ''
    for i in range(len(chunk) // width):
        colorcoderframelist = []
        colorcodegframelist = []
        colorcodebframelist = []
        tiletextframelist = []
        for tile in chunk[i*width:i*width+width]: # A for loop of all the tiles (chars) inside of the chunk (what you see on the screen at a time)
            incolorcode = False
            tiletext = ''
            colorcode = '' # Reset color code because the color code mode was just entered.
            for char in tile: # Loop everything inside of the tile to find the color seperator
                if char == '`': # If the char is the color seperator
                    if incolorcode:
                        incolorcode = False # This would trigger at the end of 255,0,255, meaning to that is the end, and the next tile is coming up so inside of color should go to false.
                    else:
                        incolorcode = True # For example if not inside of 255,0,255 yet, set inside to true.
                        continue # Don't want to print the seperator
                else:
                    if not incolorcode: # When it isn't a color, it's hopefully the char that will be printed, this should still work fine if its multiple chars, but rendering will not work so not sure why I didn't just check the 2nd char oh well.
                        tiletext += char
                if incolorcode:
                    colorcode += char # Add to color code the next char
            # colorcode would be the HEX color code that was parsed
            # tiletext is the TEXT that should be printed with that color
            colormode = 'r'
            r = '' # If this color is never filled, it is blank so the color is not printed
            g = ''
            b = ''
            for char in colorcode: # Seperate into rgb.
                if char == ',': # Checking for seperator in the rgb. Example: 255,0,0 this would trigger at the ,'s
                    # This entire block just moves to the next color code when it detects the comma in the color code
                    if colormode == 'r':
                        colormode = 'g'
                    elif colormode == 'g':
                        colormode = 'b'
                else:
                    # These duplicate if nested statments just add the color code char depending on what color it should be. 
                    if colormode == 'r':
                        r += char
                    elif colormode == 'g':
                        g += char
                    elif colormode == 'b':
                        b += char
            # Add all the color codes in seperate lists (dumb way)
            colorcoderframelist.append(r)
            colorcodegframelist.append(g)
            colorcodebframelist.append(b)
            tiletextframelist.append(tiletext)
        for i in range(len(tiletextframelist)):
            if colorcoderframelist[i] == '': # Just check one of the colors, assume if red doesn't exist the other ones don't either
                frame = frame + tiletextframelist[i] # Do not attempt to add a color when none is provided
            else:
                frame = frame + term.color_rgb(colorcoderframelist[i],colorcodegframelist[i],colorcodebframelist[i])(tiletextframelist[i])
        frame += '\n' # Add a new line before doing the next row
                
    print(term.home + frame, end="", flush=True)
    time.sleep(1)