from collections import defaultdict
from itertools import product


def get_state(coord, g, d):
    neighbor_shifts = [-1, 0, 1]
    neighbors = product(neighbor_shifts, repeat=d)

    active_count = sum(
        g[tuple([coord[i] + n[i] for i in range(d)])] for n in neighbors
        if n != tuple([0] * d)
    )

    if g[coord] and active_count not in [2, 3]:
        return 0
    if not g[coord] and active_count == 3:
        return 1
    return g[coord]


def get_grid_dims(g, d):
    mins = []
    maxs = []
    for i in range(d):
        mins.append(min([k[i] for k, v in grid.items() if v == 1]))
        maxs.append(max([k[i] for k, v in grid.items() if v == 1]))

    return mins, maxs


# f_name = 'ex1.txt'
f_name = 'input.txt'
dims = 4

grid = defaultdict(int)
with open(f_name, 'r') as f:
    zero_dims = dims - 2
    for y, row in enumerate(f.readlines()):
        for x, col in enumerate(row.strip('\n')):
            coord = tuple([x, y] + [0] * zero_dims)
            grid[coord] = 1 if col == '#' else 0

cycles = 6

for cycle in range(1, cycles+1):
    # get max and min coordinates for each dimension, then add 1 to each and iterate
    # over the coordinates
    mins, maxs = get_grid_dims(grid, dims)

    temp_grid = defaultdict(int)
    all_coords = product(*[(range(mins[i] - 1, maxs[i] + 2)) for i in range(dims)])
    for c in all_coords:
        temp_grid[c] = get_state(c, grid, dims)

    grid = temp_grid.copy()

# we're done, spit out the number of active cubes
part1 = sum(grid.values())
print(f'Part 1, active cubes: {part1}')

# Part 1: 286
# Part 2: 960
