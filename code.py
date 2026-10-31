import time
import blessed

term = blessed.Terminal()
results = []

# Test 1: Single output
start = time.perf_counter()
print("HELLO WORLD", flush=True)
results.append(("Single output", (time.perf_counter() - start) * 1000))

# Test 2: 1000 outputs
start = time.perf_counter()

for i in range(1000):
    print(str(i), end="", flush=True)

results.append(("1000 outputs", (time.perf_counter() - start) * 1000))

# Test 3: Large output
data = "X" * 10000

start = time.perf_counter()
print(data, flush=True)
results.append(("Large output", (time.perf_counter() - start) * 1000))

# Test 4: Input
print("\nPress any key")

start = time.perf_counter()

with term.cbreak():
    key = term.inkey(timeout=10)

results.append(("Input response", (time.perf_counter() - start) * 1000))

# Save results
with open("terminal_test.txt", "w") as file:
    for name, timing in results:
        file.write(name + ": " + str(round(timing, 3)) + " ms\n")

print("\nResults saved to terminal_test.txt")