# Load any required modules. Most commonly used:

import re

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
    """Solve part 1. Return the required output value."""
    regex = re.compile(r"(\d)")
    digits = []
    for line in puzzle_input:
        matches = regex.findall(line.strip())
        if matches:
            digits.append(list(map(int, matches)))

    # take first and last digit of the input
    result = sum(int(str(line[0]) + str(line[-1])) for line in digits)

    return result


s_to_d = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # use lookahead to find overlapping numbers like 'oneight': (?=)
    regex = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))")
    digits = []
    for line in puzzle_input:
        line_digits = []
        matches = regex.findall(line.strip())
        if matches:
            for m in matches:
                if m in s_to_d:
                    line_digits.append(s_to_d[m])
                else:
                    line_digits.append(int(m))
            digits.append(line_digits)

    # take first and last digit of the input
    result = sum(int(str(line[0]) + str(line[-1])) for line in digits)

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/01.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 10:21  End: 10:26
# Part 2: Start: 10:26 End: 11:14

# Elapsed time to run part1: 0.00148 seconds.
# Part 1: 57346
# Elapsed time to run part2: 0.00297 seconds.
# Part 2: 57345
