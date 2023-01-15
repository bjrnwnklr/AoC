# Load any required modules. Most commonly used:

import re

# from collections import defaultdict
# from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input.append(line.strip())

    regex = re.compile(r"(\d+)")

    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            matches = regex.findall(line.strip())
            if matches:
                puzzle_input.append(list(map(int, matches)))

    return puzzle_input


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    Multiply blueprint ID with largest number of geodes that can be
    opened in 24 minutes. Add up all these products.

    Run a BFS for each blueprint.
    State of a BFS is
    - minute
    - number of robots of each type
    - number of ore and clay
    - number of geodes opened

    Possible optimization:
    - consider same state if number of robots is same for the minute
      and discard if number of ore, clay and geodes is larger
    - or, total number of ore and clay (incl spent on robots) is larger
      for the same minute (regardless of how spent it)
    """
    print(puzzle_input)

    return 1


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/19.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 17:00 End:
# Part 2: Start:  End:
