# Load any required modules. Most commonly used:

import re

# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """

    # Extract ints from the input
    #
    # signed ints
    # regex = re.compile(r"(-?\d+)")
    #
    # unsigned ints
    regex = re.compile(r"(\d+)")

    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            matches = regex.findall(line.strip())
            if matches:
                puzzle_input.append(list(map(int, matches)))

    return puzzle_input


def safe_report(l):
    """Calculates if all numbers are either increasing or decreasing, and if
    the absolute increments are all between 1 and 3."""
    increments = [l[i] - l[i + 1] for i in range(len(l) - 1)]
    # check if all increments are positive, or all negative
    if all(n > 0 for n in increments) or all(n < 0 for n in increments):
        # check if all absolute increments are between 1 and 3
        if all(1 <= abs(n) <= 3 for n in increments):
            return True
    return False


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    result = sum(safe_report(l) for l in puzzle_input)
    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    result = 0
    for l in puzzle_input:
        if safe_report(l):
            result += 1
        # report is unsafe, try different combinations of subgroups
        else:
            for i in range(len(l)):
                new_list = l[:i] + l[i + 1 :]
                if safe_report(new_list):
                    result += 1
                    break
    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/02.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 11:49 End: 12:06
# Part 2: Start: 12:07 End: 12:23

# Elapsed time to run part1: 0.00157 seconds.
# Part 1: 631
# Elapsed time to run part2: 0.00536 seconds.
# Part 2: 665
