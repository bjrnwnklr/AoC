# Load any required modules. Most commonly used:

import re
import math
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    regex = re.compile(r'(-?\d+)')
    with open(f_name, 'r') as f:
        matches = regex.findall(f.readline().strip())
        puzzle_input = list(map(int, matches))

    return puzzle_input


def calc_x(vx, n):
    """Calculates the x value given velocity vx and steps n."""
    steps_x = min(vx, n)
    return steps_x * vx - ((steps_x - 1) * steps_x) // 2


def calc_y(vy, n):
    """Calculates the y value given velocity vy and steps n."""
    return n * vy - ((n - 1) * n) // 2


def y_in_target(y, target):
    """True if y is within the target."""
    return target[2] <= y <= target[3]


def x_in_target(x, target):
    """True if x is within the target."""
    return target[0] <= x <= target[1]


def in_target(x, y, target):
    """True if both x and y are within the target."""
    return x_in_target(x, target) and y_in_target(y, target)


def calc_max_y_positions(vx, vy, n):
    """Calculate the maximum of y positions given velocities vx and vy for steps 1-n."""
    temp_vy = vy
    y = 0
    results = []
    for i in range(1, n + 1):
        y += temp_vy
        temp_vy -= 1
        results.append(y)

    return max(results)


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    valid_velocities = set()
    min_x, max_x, min_y, max_y = puzzle_input

    for vy in range(min_y, abs(min_y) + 1):
        for n in range(1, 2 * max_x):
            y = calc_y(vy, n)
            if y_in_target(y, puzzle_input):
                for vx in range(1, max_x + 1):
                    x = calc_x(vx, n)
                    if in_target(x, y, puzzle_input):
                        valid_velocities.add((vx, vy, n))

    vx_best, vy_best, n_best = max(valid_velocities, key=lambda x: x[1])
    return calc_max_y_positions(vx_best, vy_best, n_best)


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    valid_velocities = set()
    min_x, max_x, min_y, max_y = puzzle_input

    for vy in range(min_y, abs(min_y) + 1):
        for n in range(1, 2 * max_x):
            y = calc_y(vy, n)
            if y_in_target(y, puzzle_input):
                for vx in range(1, max_x + 1):
                    x = calc_x(vx, n)
                    if in_target(x, y, puzzle_input):
                        valid_velocities.add((vx, vy))

    return len(valid_velocities)


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/17.txt')
    # puzzle_input = load_input('testinput/17_1_1.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 10:26 End: 15:45
# Part 2: Start: 15:45 End: 17:07

# First ugly solution takes too long to find the part 1 result:
# Elapsed time to run part1: 4.19220 seconds.
# Part 1: 9730

# Elapsed time to run part1: 3.23388 seconds.
# Part 1: 9730
# Elapsed time to run part2: 12.96972 seconds.
# Part 2: 4110

# Optimized by first finding vy, then finding matching vx.
# Elapsed time to run part1: 0.56029 seconds.
# Part 1: 9730
# Elapsed time to run part2: 0.55905 seconds.
# Part 2: 4110

# Further optimized by limiting n range to 2 * max_x
# Elapsed time to run part1: 0.04279 seconds.
# Part 1: 9730
# Elapsed time to run part2: 0.04189 seconds.
# Part 2: 4110
