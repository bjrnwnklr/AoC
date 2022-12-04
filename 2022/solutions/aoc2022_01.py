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
        return f.read()


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    max_calories = 0
    calories = 0

    blocks = puzzle_input.split("\n\n")

    for block in blocks:
        for line in block.strip().split("\n"):
            calories += int(line.strip())

        max_calories = max(calories, max_calories)
        calories = 0

    return max_calories


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    calories_list = []
    calories = 0

    blocks = puzzle_input.split("\n\n")

    for block in blocks:
        for line in block.strip().split("\n"):
            calories += int(line.strip())

        calories_list.append(calories)
        calories = 0

    return sum(sorted(calories_list, reverse=True)[:3])


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/01.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 16:00 End: 16:09
# Part 2: Start: 16:10 End: 16:13

# Elapsed time to run part1: 0.00040 seconds.
# Part 1: 66616
# Elapsed time to run part2: 0.00039 seconds.
# Part 2: 199172
