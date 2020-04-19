# AOC 2019, day 24. Part 2.
import logging
from collections import defaultdict

def count_adjacent(r, c, l):

    result = 0
    # skip the middle tile
    if (r, c) != (2, 2):
        neighbors = [(r-1, c), (r, c+1), (r+1, c), (r, c-1)]
        for n in neighbors:
            logging.debug(f'Checking neighbor {n} for ({r}, {c}) on level {l}.')
            # check if the neighbor is a middle tile - process differently
            if n == (2, 2):
                next_layer = l + 1
                # determine which row / column in next layer we look at
                if r == 1 or r == 3:
                    next_r = 0 if r == 1 else 4
                    next_neighbors = [(next_r, i) for i in range(n_cols)]
                elif c == 1 or c == 3:
                    next_c = 0 if c == 1 else 4
                    next_neighbors = [(i, next_c) for i in range(n_rows)]

                # calculate sum of neighbors
                result += sum(levels[next_layer][x[0]][x[1]] for x in next_neighbors)

            # check if the neighbor is an outside tile - process differently
            elif n[0] < 0 or n[0] >= n_rows:
                next_layer = l - 1
                # determine which side we need to check in next layer
                next_r = 1 if r == 0 else 3
                result += levels[next_layer][next_r][2]
                logging.debug(f'Row neighbor on outer level for ({r}, {c}) on level {l}: {n}. Result: {result}')
            elif n[1] < 0 or n[1] >= n_cols:
                next_layer = l - 1
                # determine which side we need to check in next layer
                next_c = 1 if c == 0 else 3
                result += levels[next_layer][2][next_c]
                logging.debug(f'Column neighbor on outer level for ({r}, {c}) on level {l}: {n}. Result: {result}')
            else:
                result += levels[l][n[0]][n[1]]

    logging.debug(f'Adj count for ({r}, {c}) on layer {l}: {result}')
    return result


def grid_count(grid, l):
    logging.debug(f'Counting adjacents on level {l}.')
    return [
        [count_adjacent(r, c, l) for c in range(n_cols)]
        for r in range(n_rows)
    ]


def process_state(grid, l, bugs_count):
    logging.debug(f'Processing level {l}.')

    # we can update the grid directly
    for r in range(n_rows):
        for c in range(n_cols):
            # check if space is a bug
            if grid[r][c]:
                # if exactly one bug next to it, bug stays alive
                grid[r][c] = True if bugs_count[r][c] == 1 else False
            else:
                # if one or two bugs next to it, space gets infested
                grid[r][c] = True if 1 <= bugs_count[r][c] <= 2 else False

def print_grid(grid, l):
    logging.debug(f'Printing grid level {l}')
    for r in range(n_rows):
        logging.debug(''.join('#' if grid[r][c] else '.' for c in range(n_cols)))

    logging.debug('\n')

#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    f_name = 'input.txt'

    with open(f_name) as f:
        grid = [
            list(
                map(
                    lambda x: True if x == '#' else False, 
                    list(l.strip('\n'))))
            for l in f.readlines()]


    n_rows = len(grid)
    n_cols = len(grid[0])

    # define an empty default grid
    levels = defaultdict(lambda: [[False for _ in range(n_cols)] for _ in range(n_rows)])
    levels[0] = grid

    # number of epochs
    minutes = 200

    for epoch in range(minutes):
        
        min_level = min(levels.keys())
        max_level = max(levels.keys())
        logging.debug(f'EPOCH: {epoch}. Min: {min_level}, Max: {max_level}')

        bugs_counts = dict()

        # first count the adjacent bugs for each level...
        for l in range(min_level - 1, max_level + 2):
            bugs_counts[l] = grid_count(levels[l], l)

        # ...then process and update all levels
        for l in range(min_level - 1, max_level + 2):
            process_state(levels[l], l, bugs_counts[l])
            # if no bugs on this level, delete it. Save processing time...
            if sum(sum(row) for row in levels[l]) == 0:
                del levels[l]

    # count the bugs across all levels
    result = sum(sum(row) for grid in levels.values() for row in grid)
    logging.info(f'Number of bugs after {minutes} minute(s): {result}')

    logging.info(f'Number of layers: {len(levels)}')

    for r in range(n_rows):
        logging.info(''.join('#' if levels[0][r][c] else '.' for c in range(n_cols)))
        
# part 2 result: 1963