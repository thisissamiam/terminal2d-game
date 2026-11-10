import blessed
import time

term = blessed.Terminal()

print(term.clear)
print("Press W, release it, and watch the output.")
print("Press Q to quit.\n")

with term.cbreak():
    while True:
        key = term.inkey(timeout=0.01)

        if key:
            print(
                "Key:", repr(key),
                "| Name:", key.name,
                "| Time:", round(time.perf_counter(), 4),
                flush=True
            )

            if key.lower() == 'q':
                break