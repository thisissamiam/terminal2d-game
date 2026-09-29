from blessed import Terminal
import time

term = Terminal()

x = 40.0
y = 10.0

vx = 0.0
vy = 0.0

left_until = 0
right_until = 0

HOLD_TIME = 0.08

WIDTH = 80
GROUND_Y = 20

last_time = time.time()

with term.cbreak(), term.hidden_cursor():
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

            elif key == " " and y >= GROUND_Y:
                vy = -15

            elif key.lower() == "q":
                break

        vx = 0

        if now < left_until:
            vx -= 20

        if now < right_until:
            vx += 20

        vy += 40 * dt

        x += vx * dt
        y += vy * dt

        if y > GROUND_Y:
            y = GROUND_Y
            vy = 0

        x = max(0, min(WIDTH - 1, x))

        print(term.home + term.clear, end="")

        for row in range(GROUND_Y + 1):
            if row == int(y):
                print(" " * int(x) + "@")
            elif row == GROUND_Y:
                print("_" * WIDTH)
            else:
                print()

        time.sleep(1 / 60)