# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    - split each line into equal halves
    - compare which letters appear in both
    - calc sum of letters
        - a..z == 1..26
        - A..Z == 27..52
    """
    result = 0
    for line in puzzle_input:
        half = len(line) // 2
        assert 2 * half == len(line)
        l, r = set(line[:half]), set(line[half:])

        # compare letters using set intersection
        intersect = l & r

        # calculate value
        # ord('A') == 65
        # ord('a') == 97
        # lower case = ord(c) - 96
        # upper case = ord(C) - 38
        for c in intersect:
            if c.islower():
                result += ord(c) - 96
            else:
                result += ord(c) - 38

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    - every set of three lines in input corresponds to a single
        group
    - each group can have different badge item type
    """
    result = 0
    for i in range(0, len(puzzle_input) - 2, 3):
        r1, r2, r3 = (
            set(puzzle_input[i]),
            set(puzzle_input[i + 1]),
            set(puzzle_input[i + 2]),
        )
        # compare letters using set intersection
        intersect = r1 & r2 & r3

        # calculate value
        # ord('A') == 65
        # ord('a') == 97
        # lower case = ord(c) - 96
        # upper case = ord(C) - 38
        for c in intersect:
            if c.islower():
                result += ord(c) - 96
            else:
                result += ord(c) - 38

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/03.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 13:49 End: 14:04
# Part 2: Start: 14:05 End: 14:12
