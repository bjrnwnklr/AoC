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
    # rules / constraints
    config = {"red": 12, "green": 13, "blue": 14}
    # parse input into games and sets of cubes
    result = 0
    for line in puzzle_input:
        # possible value
        possible = True
        # find game id
        match = re.search(r"(\d+)", line)
        if match:
            game = int(match[0])
        # find other digits with cubes
        matches = re.findall(r"((\d+) (red|green|blue))", line)
        if matches:
            for m in matches:
                _, n, c = m
                n = int(n)
                # check if this is a possible value
                if n > config[c]:
                    possible = False

        if possible:
            result += game

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # parse input into games and sets of cubes
    result = 0
    for line in puzzle_input:
        power = 1
        max_colors = {"red": 0, "green": 0, "blue": 0}
        # find game id
        match = re.search(r"(\d+)", line)
        if match:
            game = int(match[0])
        # find other digits with cubes
        matches = re.findall(r"((\d+) (red|green|blue))", line)
        if matches:
            for m in matches:
                _, n, c = m
                n = int(n)
                # check for maximum value of each color
                max_colors[c] = max(max_colors[c], n)
        for n in max_colors.values():
            power *= n
        result += power

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

# Part 1: Start: 11:21 End: 11:40
# Part 2: Start: 11:41 End: 11:47

# Elapsed time to run part1: 0.00087 seconds.
# Part 1: 2176
# Elapsed time to run part2: 0.00078 seconds.
# Part 2: 63700
