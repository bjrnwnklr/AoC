# Load any required modules. Most commonly used:

# import re
from collections import Counter

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
            puzzle_input.append(list(map(int, line.strip().split())))

    return puzzle_input


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # transpose lists
    left, right = [*zip(*puzzle_input)]
    # sort both sides, then zip up
    s_left = sorted(left)
    s_right = sorted(right)
    result = 0
    for l, r in zip(s_left, s_right):
        result += abs(l - r)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # transpose lists
    left, right = [*zip(*puzzle_input)]
    # count each number in each side, then calculate the score
    left_counter = Counter(left)
    right_counter = Counter(right)
    result = 0
    for n in left_counter:
        result += n * left_counter[n] * right_counter[n]

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

# Part 1: Start: 15:10 End: 15:26
# Part 2: Start: 15:27 End: 15:35

# Elapsed time to run part1: 0.00036 seconds.
# Part 1: 1319616
# Elapsed time to run part2: 0.00044 seconds.
# Part 2: 27267728
