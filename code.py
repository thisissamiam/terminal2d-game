import curses
from opensimplex import OpenSimplex
game = None # Create empty game screen
world = [] # Create the 2d world, starting as nothing
seed = random.randint(0, 100000000) # Generate the seed, determines what is generated
gen = OpenSimplex(seed=seed)
def gameloop():
    while True:
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
