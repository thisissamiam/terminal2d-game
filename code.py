from blessed import Terminal
import time

term = Terminal()

WIDTH = 80
HEIGHT = 25

x = 40.0
y = 20.0

vx = 0.0
vy = 0.0

left_until = 0
right_until = 0

HOLD_TIME = 0.08

last_time = time.time()

with term.fullscreen(), term.cbreak(), term.hidden_cursor():

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

            elif key == " " and y >= HEIGHT - 2:
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

        if y > HEIGHT - 2:
            y = HEIGHT - 2
            vy = 0

        if x < 0:
            x = 0

        if x > WIDTH - 1:
            x = WIDTH - 1

        lines = []

        for row in range(HEIGHT):
            if row == HEIGHT - 1:
                lines.append("_" * WIDTH)
                continue

            line = [" "] * WIDTH

            if row == int(y):
                line[int(x)] = "@"

            lines.append("".join(line))

        frame = "\n".join(lines)

        print(term.home + frame, end="", flush=True)

        time.sleep(1 / 60)