import curses
import random
from opensimplex import OpenSimplex
import blessed
game = None # Create empty game screen
world = [] # Create the 2d world, starting as nothing
seed = random.randint(0, 100000000) # Generate the seed, determines what is generated
gen = OpenSimplex(seed=seed)
term = blessed.Terminal() # Term is basicly the terminal, allows editing and getting data about the terminal.
for i in range(256):
    print(f"\033[48;2;{i};0;{255-i}m \033[0m", end="")
print()
def gameloop():
    # Chunk Settings
    width = 100
    height = 30
    for y in range(height):
            row = []
            for x in range(width):
                row.append(' ')
            world.append(row)
    game.refresh()

def main(stdscr):
    global game
    game = stdscr
    gameloop()
curses.wrapper(main)
