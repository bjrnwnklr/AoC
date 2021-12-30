# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file. Specify the relative path 
    if loading files from a subdirectory, e.g. for loading test inputs, specify
    `test/test1_1.txt`.

    Depending on the puzzle, change how the lines in the file are parsed, what format
    the extracted values have etc.

    Args:
        f_name (String): File name of the input file.

    Returns:
        List: A list of the inputs read in.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(int(line.strip()))

    return puzzle_input


def calc_increase(inp, n=1):
    # return sum(
    #     1 for i in range(len(inp) - n) if sum(inp[i:i+n]) < sum(inp[i+1:i+1+n])
    # )

    # a + b + c < b + c + d if a < d...
    return sum(n1 < n2 for n1, n2 in zip(inp, inp[n:]))


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    return calc_increase(puzzle_input)


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return calc_increase(puzzle_input, n=3)


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/01.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: 1832
# Part 2: 1858
