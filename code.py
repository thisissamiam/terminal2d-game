import random
from opensimplex import OpenSimplex
import blessed
import time
world = [] # Create the 2d world, starting as nothing
seed = random.randint(0, 100000000) # Generate the seed, determines what is generated
gen = OpenSimplex(seed=seed)
term = blessed.Terminal() # Term is basicly the terminal, allows editing and getting data about the terminal.
print(term.clear) # Clear the screen before starting the game cuz yeah
# Chunk Settings
width = 100
height = 30
centerx = width // 2 # Get the center of the screen, generate from the center so you have 0,0 in a spot that makes sense, and spawn the player at 0,0 as well.
chunk = [] # Need to make it before generateterrain function so it can be used by other functions
def generateterrain():
    global worldx
    global chunk # Get chunk that was defined outside of function
    chunk = [' '] * width * height # Reset current chunk data before calculating terrain
    for x in range(width):
        topheight = 15 - int(gen.noise2((x+worldx+centerx) / 10.0, 0) * 10)
        for y in range(topheight, height): # Places terrain from the generated height (topheight) to the bottom of the screen (the ground)
            chunk[y * width + x] = '#' # No colors at first
    
    # This is where stuff can be changed in the chunk, colors, stuff on screen, characters, ect.

def findspawnlocation():
    global chunk
    global centerx
    for y in range(height):
        if chunk[centerx + y * width] != ' ': # Find the first ground
            return y-1

def move():
    global worldx
    key = term.inkey(timeout=0.1)
    if key == 'd':
        worldx += 1

def render():
    frame = ''
    for row in range(height): # Every row goes through this
        colorcoderframelist = []
        colorcodegframelist = []
        colorcodebframelist = []
        tiletextframelist = []
        for tile in chunk[row*width:row*width+width]: # A for loop of all the tiles (chars) inside of the chunk (what you see on the screen at a time)
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
        for tile in range(len(tiletextframelist)): # Loop all the tiles inside of the tile list
            if colorcoderframelist[tile] == '': # Just check one of the colors, assume if red doesn't exist the other ones don't either
                frame = frame + tiletextframelist[tile] # Do not attempt to add a color when none is provided
            else:
                frame = frame + term.color_rgb(colorcoderframelist[tile],colorcodegframelist[tile],colorcodebframelist[tile])(tiletextframelist[tile])
        frame += '\n' # Add a new line before doing the next row
                
    print(term.home + frame, end="", flush=True) # Basicly clear the screen no idea what half of it does though.
def gameloop():
    with term.cbreak(), term.hidden_cursor():
        while True:
            move()
            generateterrain() # Makes the terrain and puts it into list chunk
            chunk[centerx + playery * width] = '!'
            render()

worldx = -50 # generate terrain needs this to know where to start
generateterrain() # Call this before game loop, must do this so the character can be created before the game is started
playery = findspawnlocation() # Find a safe spot to place the player
render()
gameloop()