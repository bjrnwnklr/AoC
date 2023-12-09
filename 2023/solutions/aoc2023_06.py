# Load any required modules. Most commonly used:

import re

# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    regex = re.compile(r"(\d+)")

    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            matches = regex.findall(line.strip())
            if matches:
                puzzle_input.append(list(map(int, matches)))

    return puzzle_input


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    result = 1
    for t, d in zip(*puzzle_input):
        win_count = 0
        for t_press in range(t):
            t_race = t - t_press
            speed = t_press
            dist = t_race * speed
            if dist > d:
                win_count += 1
        result *= win_count

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    result = 1
    t = int("".join(str(x) for x in puzzle_input[0]))
    d = int("".join(str(x) for x in puzzle_input[1]))
    win_count = 0
    for t_press in range(t):
        t_race = t - t_press
        speed = t_press
        dist = t_race * speed
        if dist > d:
            win_count += 1
    result *= win_count

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/06.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 15:10 End: 15:19
# Part 2: Start: 15:20 End: 15:22

# Elapsed time to run part1: 0.00002 seconds.
# Part 1: 1710720
# Elapsed time to run part2: 2.99072 seconds.
# Part 2: 35349468
