from opensimplex import OpenSimplex
import time

digits = 20

while True:
    seed = 10 ** digits

    start = time.perf_counter()

    try:
        gen = OpenSimplex(seed=seed)
        elapsed = time.perf_counter() - start

        print(digits, 'digits: works |', round(elapsed * 1000, 2), 'ms')

    except Exception as e:
        print(digits, 'digits: failed |', e)
        break

    digits += 10