# Load any required modules. Most commonly used:

import re

# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    # unsigned ints
    regex = re.compile(r"(-?\d+)")

    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            matches = regex.findall(line.strip())
            if matches:
                puzzle_input.append(list(map(int, matches)))

    return puzzle_input


def get_diff(seq):
    """Get a list of the differences between each two pairs of numbers."""
    diff = []
    for i in range(len(seq) - 1):
        diff.append(seq[i + 1] - seq[i])
    return diff


def is_all_zeroes(seq):
    """Return if all numbers in the sequence are zeroes."""
    return all(x == 0 for x in seq)


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    result = 0
    for line in puzzle_input:
        seq = line[:]
        last_nums = []
        while not is_all_zeroes(seq):
            last_nums.append(seq[-1])
            seq = get_diff(seq)

        # reached all zeroes, now work
        # backwards by adding to last_nums
        # this can be achieved by adding the last numbers together
        result += sum(last_nums)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    result = 0
    for line in puzzle_input:
        seq = line[:]
        first_nums = []
        while not is_all_zeroes(seq):
            first_nums.append(seq[0])
            seq = get_diff(seq)

        # reached all zeroes, now work
        # backwards by adding to last_nums
        z = 0
        for x in first_nums[::-1]:
            z = x - z
        result += z

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/09.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 16:53 End: 17:08
# Part 2: Start: 17:09 End: 17:23

# Elapsed time to run part1: 0.00271 seconds.
# Part 1: 1877825184
# Elapsed time to run part2: 0.00270 seconds.
# Part 2: 1108
