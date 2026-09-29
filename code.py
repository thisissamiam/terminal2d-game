from blessed import Terminal

term = Terminal()

while True:
    key = term.inkey()

    if key:
        print(repr(key))