# Load any required modules. Most commonly used:

import re
from utils.aoctools import aoc_timer
import numpy as np


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    regex = re.compile(r'(\d+)')
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append([int(n)
                                for n in re.findall(regex, line.strip())])

    return puzzle_input


def diagonal(x1, y1, x2, y2, a):
    # sort pairs by minimum y coordinate (start with upper row)
    pos1 = min([(x1, y1), (x2, y2)], key=lambda x: x[1])
    pos2 = max([(x1, y1), (x2, y2)], key=lambda x: x[1])

    # if x1 > x2, we need to walk backwards on the x axis
    direction = -1 if pos1[0] > pos2[0] else 1

    for i in range(pos2[1] + 1 - pos1[1]):
        a[(pos1[1] + i, pos1[0] + (direction * i))] += 1


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    # get the dimensions of the grid
    xs = [l[0] for l in puzzle_input] + [l[2] for l in puzzle_input]
    ys = [l[1] for l in puzzle_input] + [l[3] for l in puzzle_input]
    xmax = max(xs)
    ymax = max(ys)

    grid = np.zeros((xmax + 1, ymax + 1))

    # go through all lines
    # discard any line where !(x1 == x2 or y1 == y2)
    for x1, y1, x2, y2 in puzzle_input:
        if (x1 == x2 or y1 == y2):
            # x1 / x2 and y1 / y2 need to be sorted by size, otherwise numpy won't mark them
            # correctly
            r1, r2 = min([y1, y2]), max([y1, y2])
            c1, c2 = min([x1, x2]), max([x1, x2])
            grid[r1:r2+1, c1:c2+1] += 1

    # find the points > 2
    dangerous = (grid >= 2).sum()

    return dangerous


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    # get the dimensions of the grid
    xs = [l[0] for l in puzzle_input] + [l[2] for l in puzzle_input]
    ys = [l[1] for l in puzzle_input] + [l[3] for l in puzzle_input]
    xmax = max(xs)
    ymax = max(ys)

    grid = np.zeros((xmax + 1, ymax + 1))

    # go through all lines
    for x1, y1, x2, y2 in puzzle_input:
        if (x1 == x2 or y1 == y2):
            # x1 / x2 and y1 / y2 need to be sorted by size, otherwise numpy won't mark them
            # correctly
            r1, r2 = min([y1, y2]), max([y1, y2])
            c1, c2 = min([x1, x2]), max([x1, x2])
            grid[r1:r2+1, c1:c2+1] += 1
        else:
            # a diagonal line, calculate the correct grid points
            diagonal(x1, y1, x2, y2, grid)

    # find the points > 2
    dangerous = (grid >= 2).sum()

    return dangerous


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/05.txt')
    # puzzle_input = load_input('testinput/05_1_1.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 15:48 End: 16:21
# Part 2: Start: 15:22 End: 17:32 (ca 1.5 hours)
