# AOC 2019, day 24. Part 2.
import logging
from collections import defaultdict

def count_adjacent(r, c, l):

    result = 0
    # skip the middle tile
    if (r, c) != (2, 2):
        neighbors = [(r-1, c), (r, c+1), (r+1, c), (r, c-1)]
        for n in neighbors:
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
            elif n[0] < 0 or n[0] >= n_rows or n[1] < 0 or n[1] >= n_cols:
                next_layer = l - 1
                # determine which side we need to check in next layer
                if r == 0 or r == n_rows - 1:
                    next_r = 1 if r == 0 else 3
                    result += levels[next_layer][next_r][c]
                elif c == 0 or c == n_cols - 1:
                    next_c = 1 if c == 0 else 3
                    result += levels[next_layer][r][next_c]

            else:
                result += levels[l][n[0]][n[1]]

    return result


def grid_count(grid, l):
    return [
        [count_adjacent(r, c, l) for c in range(n_cols)]
        for r in range(n_rows)
    ]


def process_state(l, levels):
    logging.debug(f'processing level {l}.')
    grid = levels[l]
    bugs_count = grid_count(grid, l)

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

#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    f_name = 'example1.txt'

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

    print(levels) 
    # print(levels[-1])



    for epoch in range(1):
        
        min_level = min(levels.keys())
        max_level = max(levels.keys())
        logging.debug(f'EPOCH: {epoch}. Min: {min_level}, Max: {max_level}')

        for l in range(min_level - 1, max_level + 2):
            process_state(l, levels)
            print(f'Level {l}: {levels[l]}')
        
