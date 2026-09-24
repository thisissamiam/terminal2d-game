import time

frames = 0
start = time.time()

while time.time() - start < 5:
    # pretend this is your game update/render
    for x in range(100):
        pass

    frames += 1

print("FPS:", frames / 5)
