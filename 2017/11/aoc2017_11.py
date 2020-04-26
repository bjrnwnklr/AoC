# hex ed

# use a BFS to find shortest path?
from collections import defaultdict, deque


f_name = 'input.txt'

with open(f_name, 'r') as f:
    orig_path = [x for x in f.readline().strip('\n').split(',')]

# trace path along hex grid, using the cube coordinates described at http://redblobgames.com/grids/hexagons
# x = top left to bottom right axis. Going to NW, values decrease, going to SE, values increase
# y = top to bottom axis. Going up (N), values decrease, going down (S) values increase
# z = bottom left to top right axis. Going to SW, values decrease, going to NE, values increase


directions = {
    'n': (0, 1, -1),
    'ne': (1, 0, -1),
    'se': (1, -1, 0),
    's': (0, -1, 1),
    'sw': (-1, 0, 1),
    'nw': (-1, 1, 0)
}

start = (0, 0, 0)
max_dist = 0
curr_pos = start
# trace path taken and see where we end up
for step in orig_path:
    curr_pos = tuple(curr_pos[i] + directions[step][i] for i in range(3))
    max_dist = max(max_dist, max(curr_pos))

print(f'Arrived at {curr_pos} after {len(orig_path)} steps.')
# number of steps is the maximum of the three coordinates.
print(f'Number of steps required: {max(curr_pos)}')
print(f'Max distance from starting position: {max_dist}')

# part 1: 643
# part 2: 1471
