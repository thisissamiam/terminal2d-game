from blessed import Terminal
import time

term = Terminal()

x = 40

left_until = 0
right_until = 0

HOLD_TIME = 0.08
MOVE_SPEED = 30

last_time = time.time()

with term.cbreak(), term.hidden_cursor():
    print(term.clear)

    while True:
        now = time.time()
        dt = now - last_time
        last_time = now

        key = term.inkey(timeout=0)

        if key:
            if key.lower() == "a":
                left_until = now + HOLD_TIME

            elif key.lower() == "d":
                right_until = now + HOLD_TIME

            elif key.lower() == "q":
                break

        if now < left_until:
            x -= MOVE_SPEED * dt

        if now < right_until:
            x += MOVE_SPEED * dt

        if x < 0:
            x = 0

        if x > 79:
            x = 79

        print(term.home + (" " * int(x)) + "@", end="", flush=True)

        time.sleep(1 / 60)