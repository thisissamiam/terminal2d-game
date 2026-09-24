import curses

game = None # Create empty game screen

def gameloop():
    while True:
        
        game.refresh()

def main(stdscr):
    global game
    game = stdscr
    gameloop()
curses.wraper(main)
