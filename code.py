import time
import blessed
import sys

term = blessed.Terminal()

print(term.clear)

# Test 1: Single output
print("TEST 1: Single output")

start = time.perf_counter()
print(term.home + "HELLO WORLD", flush=True)
end = time.perf_counter()

print("Print time:", (end - start) * 1000, "ms")


# Test 2: Repeated output
print("\nTEST 2: 1000 outputs")

start = time.perf_counter()

for i in range(1000):
    print(term.home + str(i), end="", flush=True)

end = time.perf_counter()

print("\n1000 outputs:", (end - start) * 1000, "ms")


# Test 3: Large output
print("\nTEST 3: Large output")

data = "X" * 100000

start = time.perf_counter()
print(data, flush=True)
end = time.perf_counter()

print("Large output time:", (end - start) * 1000, "ms")


# Test 4: Terminal input response
print("\nTEST 4: Press any key")

start = time.perf_counter()

with term.cbreak():
    key = term.inkey(timeout=10)

end = time.perf_counter()

print("Input response:", (end - start) * 1000, "ms")
print("Key:", repr(key))