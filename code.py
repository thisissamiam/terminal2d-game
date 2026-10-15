
import time
import gc
from opensimplex import OpenSimplex
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# Width increases dramatically. Height increases too.
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


def generate_terrain(width, height):
    # Terrain generation is NOT included in A* timing.
    noise = OpenSimplex(seed=42)

    surface = []

    for x in range(width):
        value = noise.noise2(x * NOISE_SCALE, 0)
        ground_y = int(height * 0.55 - value * height * NOISE_HEIGHT)

        # Leave enough room above and below the surface.
        ground_y = max(2, min(height - 2, ground_y))
        surface.append(ground_y)

    # 1 = air/walkable, 0 = solid ground.
    matrix = []

    for y in range(height):
        row = []

        for x in range(width):
            row.append(1 if y < surface[x] else 0)

        matrix.append(row)

    return matrix, surface


def benchmark(width, height):
    cells = width * height

    print(f"\nGenerating {width:,} x {height:,} map "
          f"({cells:,} cells)...", flush=True)

    before = time.perf_counter()
    matrix, surface = generate_terrain(width, height)
    generation_time = time.perf_counter() - before

    # Grid creation is also excluded from A* timing.
    before = time.perf_counter()
    grid = Grid(matrix=matrix)
    setup_time = time.perf_counter() - before

    finder = AStarFinder()

    # Fly from near the left edge to near the right edge,
    # starting just above the generated terrain.
    sx = 1
    ex = width - 2
    sy = max(0, surface[sx] - 1)
    ey = max(0, surface[ex] - 1)

    start = grid.node(sx, sy)
    end = grid.node(ex, ey)

    # Warm-up search, excluded from measurements.
    grid.cleanup()
    finder.find_path(start, end, grid)

    times = []
    runs_list = []
    path_length = 0

    for i in range(REPEATS):
        grid.cleanup()

        # Only the actual A* call is timed.
        before = time.perf_counter()
        path, runs = finder.find_path(start, end, grid)
        elapsed = time.perf_counter() - before

        times.append(elapsed)
        runs_list.append(runs)
        path_length = len(path)

        print(
            f"  Run {i + 1}: {elapsed * 1000:.3f} ms "
            f"| {runs:,} nodes explored",
            flush=True
        )

    average = sum(times) / len(times)

    result = {
        "width": width,
        "height": height,
        "cells": cells,
        "generation": generation_time,
        "setup": setup_time,
        "average": average,
        "fastest": min(times),
        "slowest": max(times),
        "nodes": sum(runs_list) / len(runs_list),
        "path_length": path_length,
    }

    del finder, grid, matrix, surface
    gc.collect()

    return result


print("A* TERRAIN SCALING BENCHMARK")
print("=" * 60)

results = []

for width, height in SIZES:
    try:
        results.append(benchmark(width, height))
    except MemoryError:
        print("Not enough memory; stopping benchmark.")
        break

print("\n\nSCALING SUMMARY")
print("=" * 85)
print(
    f"{'Map':>15} {'Cells':>10} {'Avg ms':>10} "
    f"{'x previous':>12} {'Nodes':>12}"
)

previous = None

for r in results:
    if previous is None:
        ratio = "-"
    elif previous["average"] == 0:
        ratio = "-"
    else:
        ratio = f"{r['average'] / previous['average']:.2f}x"

    print(
        f"{r['width']}x{r['height']: <8} "
        f"{r['cells']:>10,} "
        f"{r['average'] * 1000:>10.3f} "
        f"{ratio:>12} "
        f"{r['nodes']:>12,.0f}"
    )

    previous = r

print("\nGeneration and grid setup were excluded from search times.")
print("Compare node counts as well as time to understand scaling.")
