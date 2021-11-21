
def traverse(slope):
    pos = (0, 0)
    trees = 0

    while pos[0] < height - slope[0]:
        pos = (pos[0] + slope[0], (pos[1] + slope[1]) % width)
        if grid[pos[0]][pos[1]] == '#':
            trees += 1

    return trees



f_name = 'input.txt'
# f_name = 'ex1.txt'

with open(f_name, 'r') as f:
    grid = [[c for c in row.strip('\n')] for row in f.readlines()]

# get grid dimensions to know when we have reached the bottom and when we have reached the right end
# we will wrap around using %
height = len(grid)
width = len(grid[0])

# (row, column)
trees_pt1 = traverse((1, 3))
print(f'Part 1: Encountered {trees_pt1} trees.')

# Part 1: 195

slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
trees_pt2 = 1
for s in slopes:
    print(f'Pt2, slope: {s}')
    trees_pt2 *= traverse(s)

print(f'Part 2: Encountered product: {trees_pt2}')

# Part 2: 3772314000
