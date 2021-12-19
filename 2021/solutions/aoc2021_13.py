# Load any required modules. Most commonly used:

import re
import numpy as np
# from collections import defaultdict
# from utils.aoctools import aoc_timer


def print_array(a: np.array) -> None:
    """Print a boolean np.array"""
    c = '#'
    b = ' '

    for row in a:
        print(''.join(c if x else b for x in row))


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        top, bottom = f.read().split('\n\n')

        puzzle_input = []
        for line in top.strip().split('\n'):
            puzzle_input.append(list(map(int, line.strip().split(','))))

        folds = []
        regex = re.compile(r'([xy])=(\d+)')
        for line in bottom.strip().split('\n'):
            dir, n = regex.findall(line)[0]
            n = int(n)
            folds.append((dir, n))

    return puzzle_input, folds


# @aoc_timer
def part1(puzzle_input, folds):
    """Solve part 1. Return the required output value."""

    # get the dimensions of the array. First number is x / columns, second is y / rows.
    max_x = max(x for x, _ in puzzle_input) + 1
    max_y = max(y for _, y in puzzle_input) + 1
    tp = np.zeros((max_y, max_x), dtype=bool)
    for x, y in puzzle_input:
        tp[y, x] = True

    # get the first fold
    dir, n = folds[0]
    # axis = 0 if we fold 'up', i.e. along the y axis
    axis = 0 if dir == 'y' else 1
    # split the array into two
    a, _, b = np.split(tp, [n, n + 1], axis)

    # flip the b array along the axis
    b = np.flip(b, axis)

    # add the two arrays to each other
    tp_new = a | b

    return tp_new.sum()


# @aoc_timer
def part2(puzzle_input, folds):
    """Solve part 2. Return the required output value."""

    # get the dimensions of the array. First number is x / columns, second is y / rows.
    max_x = max(x for x, _ in puzzle_input) + 1
    max_y = max(y for _, y in puzzle_input) + 1
    tp = np.zeros((max_y, max_x), dtype=bool)
    for x, y in puzzle_input:
        tp[y, x] = True

    for dir, n in folds:
        # axis = 0 if we fold 'up', i.e. along the y axis
        axis = 0 if dir == 'y' else 1
        # split the array into two
        a, _, b = np.split(tp, [n, n + 1], axis)

        # check that the arrays have the same dimensions and extend b with zeros
        # at the bottom or right if required. Then flip around.
        if a.shape != b.shape:
            delta = a.shape[axis] - b.shape[axis]
            if axis == 0:
                # add rows
                z = np.zeros((delta, a.shape[1]), dtype=bool)
            else:
                # add columns
                z = np.zeros((a.shape[0], delta), dtype=bool)

            b = np.concatenate((b, z), axis)

        assert a.shape == b.shape

        # flip the b array along the axis
        b = np.flip(b, axis)

        # add the two arrays to each other by taking the logical OR of both
        tp = a | b

    print_array(tp)

    return 1


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input, folds = load_input('input/13.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input, folds)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input, folds)
    print(f'Part 2: {p2}')

# Part 1: Start: 14:54 End: 15:37
# Part 2: Start: 15:38 End:
