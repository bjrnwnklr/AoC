# Load any required modules. Most commonly used:

import re

# from collections import defaultdict
# from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    regex = r"(\d+)"
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            matches = re.findall(regex, line.strip())
            if matches:
                puzzle_input.append(list(map(int, matches)))

    return puzzle_input


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    In how many assignment pairs does one range fully contain the other?
    """
    result = 0
    for line in puzzle_input:
        l1, r1, l2, r2 = line
        if (l1 >= l2 and r1 <= r2) or (l2 >= l1 and r2 <= r1):
            result += 1

    return result


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/04.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 14:55 End: 15:06
# Part 2: Start: 15:07 End:
