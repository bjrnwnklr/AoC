# Load any required modules. Most commonly used:

import re
import math
# from collections import defaultdict
# from utils.aoctools import aoc_timer


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


def calc_velocity(x, y, target):
    """Calculates the velocity required to hit an (x, y) coordinate in n steps.

    Formular used is derived from

    x = sum(vx + i * dx), y = sum(vy + i * dy) for i=0..n, which can be resolved to vx and vy:
    vx = (x + sum(i * dx)) // n = (2x + (n - 1) * n) // 2n
    vy = (y + sum(i * dy)) // n = (2y + (n - 1) * n) // 2n

    However, for vx the decreases stop at 0, so we are really only summing up to vx and not n.
    Hence the actual formula for x = sum(vx + i * dx) for i=0..vx can be resolved to
    2x = vx^2 * (vx + 1).

    Using the solution to the quadratic formula (ax^2 + bx + c = 0, x = (-b +/- sqrt(b^2 - 4ac)) / 2a), 
    we can replace a and b with 1 and c with -2x to calculate vx:
    vx = (-1 + sqrt(1 - 4 * -2x)) / 2
    """
    results = []
    max_steps = max(abs(a) for a in [x, y])
    for n in range(1, max_steps + 1):
        vx, rem_x = divmod((-1 + round(math.sqrt(1 + 8 * x))), 2)
        vy, rem_y = divmod((2 * y + (n - 1) * n), (2 * n))
        if rem_x == 0 and rem_y == 0:
            print(f'x/y/n: {x}, {y}, {n}: {vx}, {vy}')
            if is_in_target(vx, vy, n, target):
                results.append((vx, vy, n))
    return results


def is_in_target(vx, vy, n, target):
    """Calculate if a pair ends up within the target (min_x, max_x, min_y, max_y)."""
    steps_x = min(vx, n)
    steps_y = n
    x = steps_x * vx - ((steps_x - 1) * steps_x) // 2
    y = steps_y * vy - ((steps_y - 1) * steps_y) // 2
    print(f'{x=}, {y=}, {vx=}, {vy=}, {n=}')
    return target[0] <= x <= target[1] and target[2] <= y <= target[3]

# @aoc_timer


def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    min_x, max_x, min_y, max_y = puzzle_input
    max_steps = max(abs(x) for x in puzzle_input)
    valid_velocities = []
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            results = calc_velocity(x, y, puzzle_input)
            valid_velocities.extend(results)

    print(set(valid_velocities))
    return 1


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
    # read the puzzle input
    # puzzle_input = load_input('input/17.txt')
    puzzle_input = load_input('testinput/17_1_1.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 10:26 End:
# Part 2: Start:  End:
