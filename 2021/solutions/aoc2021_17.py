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


def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    min_x, max_x, min_y, max_y = puzzle_input
    valid_vx = []
    valid_velocity = []
    for vx in range(1, max_x):
        temp_vx = vx
        n = 0
        x = 0
        while temp_vx > 0:
            x += temp_vx
            temp_vx -= 1
            n += 1
            if min_x <= x <= max_x:
                for ny in range(n, 10 * n):
                    for vy in range(10 * min_y, 10 * abs(min_y)):
                        sumny, rem_y = divmod((ny-1) * ny, 2)
                        if rem_y == 0:
                            y = ny * vy - sumny
                            # TODO: Need a good way to calculate x with vx - this takes any y values that fit in.
                            if min_y <= y <= max_y and min_x <= x <= max_x:
                                valid_velocity.append((vx, vy, ny))

    print(valid_velocity)

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
