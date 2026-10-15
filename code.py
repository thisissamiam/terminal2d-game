
import gc
import random
import statistics
import time

from opensimplex import OpenSimplex
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.best_first import BestFirst

# Same general map sizes as your previous benchmark.
SIZES = [
    (100, 30),
    (200, 40),
    (400, 60),
    (800, 100),
    (1600, 160),
    (3200, 240),
]

REPEATS = 3
NOISE_SCALE = 0.025
NOISE_HEIGHT = 0.18
random.seed(42)


def generate_terrain(width, height):
    # Generate your terrain before starting any search timers.
    noise = OpenSimplex(seed=42)
    surface = []

    for x in range(width):
        value = noise.noise2(x * NOISE_SCALE, 0)
        ground_y = int(
            height * 0.55 - value * height * NOISE_HEIGHT
        )
        ground_y = max(2, min(height - 2, ground_y))
        surface.append(ground_y)

    matrix = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(1 if y < surface[x] else 0)
        matrix.append(row)

    return matrix, surface


def run_search(finder, grid, start, end):
    grid.cleanup()

    before = time.perf_counter()
    path, runs = finder.find_path(start, end, grid)
    elapsed = time.perf_counter() - before

    return elapsed, runs, bool(path)


def benchmark(width, height):
    print(f"\nGenerating {width} x {height} terrain...", flush=True)

    matrix, surface = generate_terrain(width, height)

    before = time.perf_counter()
    grid = Grid(matrix=matrix)
    setup_time = time.perf_counter() - before

    # Same endpoints for both algorithms.
    sx, ex = 1, width - 2
    sy = max(0, surface[sx] - 1)
    ey = max(0, surface[ex] - 1)

    start = grid.node(sx, sy)
    end = grid.node(ex, ey)

    algorithms = {
        "A*": AStarFinder(),
        "Greedy": BestFirst(),
    }

    results = {
        name: {"times": [], "nodes": [], "successes": 0}
        for name in algorithms
    }

    # Warm both algorithms up, outside measured runs.
    for finder in algorithms.values():
        grid.cleanup()
        finder.find_path(start, end, grid)

    # Alternate order to reduce systematic timing bias.
    for repeat in range(REPEATS):
        order = list(algorithms.items())
        if repeat % 2:
            order.reverse()

        for name, finder in order:
            elapsed, runs, success = run_search(
                finder, grid, start, end
            )

            results[name]["times"].append(elapsed)
            results[name]["nodes"].append(runs)
            results[name]["successes"] += int(success)

            print(
                f"  {name:6} run {repeat + 1}: "
                f"{elapsed * 1000:9.3f} ms | "
                f"{runs:8,} nodes | "
                f"{'FOUND' if success else 'NO PATH'}",
                flush=True,
            )

    print(f"\nRESULTS — {width:,} x {height:,}")
    print(f"Cells: {width * height:,}")
    print(f"Grid setup (excluded): {setup_time:.2f} s")

    averages = {}

    for name, result in results.items():
        average = statistics.mean(result["times"])
        averages[name] = average

        print(f"\n{name}:")
        print(f"  Average: {average * 1000:.3f} ms")
        print(
            f"  Median:  "
            f"{statistics.median(result['times']) * 1000:.3f} ms"
        )
        print(
            f"  Nodes:   "
            f"{statistics.mean(result['nodes']):,.0f} average"
        )
        print(
            f"  Success: "
            f"{result['successes']}/{REPEATS}"
        )

    if averages["Greedy"] > 0:
        print(
            f"\nA* / Greedy time ratio: "
            f"{averages['A*'] / averages['Greedy']:.2f}x"
        )

    del grid, matrix, surface, algorithms
    gc.collect()


print("GREEDY BEST-FIRST vs A*")
print("=======================")

for width, height in SIZES:
    try:
        benchmark(width, height)
    except MemoryError:
        print("Out of memory; stopping.")
        break

print("\nBenchmark finished.")
