start = time.perf_counter()

for i in range(100):
    print(term.home + str(i), end='', flush=True)

print('\n100 prints:', time.perf_counter() - start)