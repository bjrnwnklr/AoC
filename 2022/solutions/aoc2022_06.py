# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input[0]


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # turn windows of 4 into a set and check length of set
    # if set has length 4, the window is a marker
    for i in range(4, len(puzzle_input)):
        window = puzzle_input[i - 4 : i]
        s = set(window)
        if len(s) == 4:
            return i
    return -1


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # turn windows of 14 into a set and check length of set
    # if set has length 14, the window is a marker
    for i in range(14, len(puzzle_input)):
        window = puzzle_input[i - 14 : i]
        s = set(window)
        if len(s) == 14:
            return i
    return -1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/06.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 19:19 End: 19:30
# Part 2: Start: 19:31 End: 19:33

# Elapsed time to run part1: 0.00046 seconds.
# Part 1: 1210
# Elapsed time to run part2: 0.00271 seconds.
# Part 2: 3476
