from collections import namedtuple
from string import ascii_uppercase

f_name = 'input.txt'

with open(f_name, 'r') as f:
    grid = [list(line.strip('\n')) for line in f.readlines()]


# down, right, up, left
directions = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]

# letters collected along path
path = []
# number of steps taken
steps = 0

Pos = namedtuple('Pos', ['r', 'c', 'dir'])

# find start and set current position
start = (0, grid[0].index('|'))
curr = Pos(*start, 0)

# find size of grid
max_r = len(grid)
max_c = len(grid[0])

while 0 <= curr.r < max_r and 0 <= curr.c < max_c:
    # move to next square, based on direction
    next_r, next_c = curr.r + directions[curr.dir][0], curr.c + directions[curr.dir][1]
    next_dir = curr.dir
    steps += 1

    # check what we found
    symbol = grid[next_r][next_c]
    if symbol in ascii_uppercase:
        # if letter - don't change direction, collect letter
        path.append(symbol)
    elif symbol == '+':
        # if plus - we need to change direction
        for i in [(curr.dir + 1) % 4, (curr.dir + 3) % 4]:
            turn_r, turn_c = next_r + directions[i][0], next_c + directions[i][1]
            # check if the next square after turning is still within the grid
            if 0 <= turn_r < max_r and 0 <= turn_c <= max_c:
                if grid[turn_r][turn_c] == ' ':
                    continue
                else:
                    next_dir = i
    elif symbol == ' ':
        # we have reached the end
        break
    # we don't need to do anything if the new symbol is '-' or '|'

    curr = Pos(next_r, next_c, next_dir)


# we have come to the end
print(f"End. Path taken: {''.join(path)}")
print(f'Steps taken: {steps}')

# part 1: PBAZYFMHT
# part 2: 16072

