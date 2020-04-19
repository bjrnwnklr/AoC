# AOC 2019, day 24
import logging

def count_adjacent(r, c):
    neighbors = [(r-1, c), (r, c+1), (r+1, c), (r, c-1)]

    return sum(grid[n[0]][n[1]] for n in neighbors if 0 <= n[0] < n_rows and 0 <= n[1] < n_cols)


def grid_count(grid):
    return [
        [count_adjacent(r, c) for c in range(n_cols)]
        for r in range(n_rows)
    ]


def process_state(grid):
    bugs_count = grid_count(grid)

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

def bio_score(grid):
    score = 0
    bit = 0
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c]:
                score += 2 ** bit
                logging.debug(f'bio_score: adding {2 ** bit} for ({r}, {c})')
            bit += 1
    logging.debug(f'bio_score: {score}')
    return score

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

    # dictionary of fingerprints for each iteration (one minute)
    fingerprints = set()

    while True:
        # print(grid)
        score = bio_score(grid)
        if score in fingerprints:
            logging.info(f'found layout with biodiversity score {score}')
            break
        fingerprints.add(score)
        process_state(grid)
        
    # we found a layout that repeats twice
    
    print(grid)

    # part 1: 32506764