# Intcode virtual machine (as of AoC2019, day 15)

import logging
from intcode import Intcode, InputInterrupt, OutputInterrupt
from collections import defaultdict


# find all valid neighbors of a scaffolding element
def neighbors(grid, coord):

    _neighbor_pos = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    neighbor_coords = [(coord[0] + n[0], coord[1] + n[1]) for n in _neighbor_pos]
    valid_neighbors = [n for n in neighbor_coords if grid[n] == '#']
    return valid_neighbors


# finding intersections - check each grid entry that is a '#', then check if the neighbors (up, down, left, right) are '#'.
def find_intersections(grid):
    # find all entries with '#'
    scaffolding = [(x, y) for (x, y), c in grid.items() if c == '#']

    intersections = [c for c in scaffolding if len(neighbors(grid, c)) == 4]
    logging.debug('{} intersections found at {}'.format(len(intersections), intersections))
    return intersections
    
#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')

    # initialize the intcode machine
    int_comp = Intcode(inp)

    raw_output = []

    while(not int_comp.done):
        try:
            int_comp._run_intcode()
        except(InputInterrupt):
            pass
        except(OutputInterrupt):
            # collect all input, process later
            raw_output.append(int_comp.out_queue.popleft())
    
    # convert to characters
    char_output = [chr(x) for x in raw_output]

    with open('grid.txt', 'w') as f:
        f.write(''.join(str(x) for x in char_output))

    grid = defaultdict(int)
    x = y = 0
    for c in char_output:
        if c == '\n':
            y += 1
            x = 0
        else:
            grid[(x, y)] = c
            if c in ['^', 'v', '<', '>']:
                grid[(x, y)] = '#'
            x += 1

    intersections = find_intersections(grid)

    part1 = sum(x * y for x, y in intersections)
    logging.info('Part 1: {}'.format(part1))

    logging.info('PART 1: End!')

    # part 1: 3608