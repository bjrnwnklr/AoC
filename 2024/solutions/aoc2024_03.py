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
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    # Extract ints from the input
    #
    # signed ints
    # regex = re.compile(r"(-?\d+)")
    #
    # unsigned ints
    # regex = re.compile(r"(\d+)")
    #
    # with open(f_name, "r") as f:
    #     puzzle_input = []
    #     for line in f.readlines():
    #         matches = regex.findall(line.strip())
    #         if matches:
    #             puzzle_input.append(list(map(int, matches)))

    return puzzle_input


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    result = 0
    for line in puzzle_input:
        line_result = 0
        matches = regex.findall(line)
        if matches:
            for m in matches:
                group_score = 1
                numbers = list(map(int, m))
                for n in numbers:
                    group_score *= n
                line_result += group_score
        result += line_result
    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|(don\'t\(\))|(do\(\))")
    result = 0
    do = True
    for line in puzzle_input:
        line_result = 0
        matches = regex.findall(line)
        if matches:
            for m in matches:
                # matches have format of ('2', '4', 'don't()', 'do()')
                if m[3] == "do()":
                    do = True
                elif m[2] == "don't()":
                    do = False
                else:
                    if do:
                        group_score = 1
                        # only take first two elements of the list as the matches will have format
                        # ('2', '4', '', '')
                        numbers = list(map(int, m[:2]))
                        for n in numbers:
                            group_score *= n
                        line_result += group_score
        result += line_result
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

# Part 1: Start: 13:30 End: 13:47
# Part 2: Start: 13:48 End: 16:25 (didnt read instructions properly...)

# Elapsed time to run part1: 0.00060 seconds.
# Part 1: 178794710
# Elapsed time to run part2: 0.00080 seconds.
# Part 2: 76729637
