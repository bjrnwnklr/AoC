from collections import defaultdict


def get_state(coord, g):
    x, y, z = coord
    neighbors = [-1, 0, 1]

    active_count = sum(
        g[(x+nx, y+ny, z+nz)] for nz in neighbors
        for ny in neighbors
        for nx in neighbors
        if (nx, ny, nz) != (0, 0, 0)
    )

    if g[coord] and active_count not in [2, 3]:
        return 0
    if not g[coord] and active_count == 3:
        return 1
    return g[coord]


def get_grid_dims(g):
    mins = []
    maxs = []
    for i in range(3):
        mins.append(min([k[i] for k, v in grid.items() if v == 1]))
        maxs.append(max([k[i] for k, v in grid.items() if v == 1]))

    return mins, maxs


def print_grid(g):
    mins, maxs = get_grid_dims(g)
    for z in range(mins[2], maxs[2] + 1):
        print(f'z={z}')
        for y in range(mins[1], maxs[1] + 1):
            print(''.join(['.' if g[(x, y, z)] == 0 else '#' for x in range(mins[0], maxs[0] + 1)]))
        print('\n')


# f_name = 'ex1.txt'
f_name = 'input.txt'

grid = defaultdict(int)
with open(f_name, 'r') as f:
    z = 0
    for y, row in enumerate(f.readlines()):
        for x, col in enumerate(row.strip('\n')):
            grid[(x, y, z)] = 1 if col == '#' else 0

# print_grid(grid)

cycles = 6

for c in range(1, cycles+1):
    # get max and min coordinates for each dimension, then add 1 to each and iterate
    # over the coordinates
    mins, maxs = get_grid_dims(grid)

    temp_grid = defaultdict(int)
    for z in range(mins[2] - 1, maxs[2] + 2):
        for y in range(mins[1] - 1, maxs[1] + 2):
            for x in range(mins[0] - 1, maxs[0] + 2):
                temp_grid[(x, y, z)] = get_state((x, y, z), grid)

    grid = temp_grid.copy()
    # print(f'After {c} cycles:\n')
    # print_grid(grid)

# we're done, spit out the number of active cubes
part1 = sum(grid.values())
print(f'Part 1, active cubes: {part1}')

# Part 1: 286
