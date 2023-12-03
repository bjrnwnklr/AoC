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
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def parse_grid_regex(inp):
    """Find numbers including their start position, and symbols.
    return two objects:
    - set of symbol coordinates
    - list of numbers with two coordinates:
        - row
        - col of the first digit
    The end of the digit can be calculated by the length
    of the number as string.
    """
    regex_num = re.compile(r"(\d+)")
    regex_sym = re.compile(r"([\@+\-#/*$%=&])")
    re_numbers = []
    re_symbols = set()
    for r, row in enumerate(inp):
        matches = regex_num.finditer(row)
        if matches:
            for m in matches:
                re_numbers.append((int(m[0]), r, m.start()))
        matches = regex_sym.finditer(row)
        if matches:
            for m in matches:
                re_symbols.add((r, m.start()))

    return re_symbols, re_numbers


def has_symbol_neighbor(n, r, c, symbols):
    """Check if the number n with starting pos (r, c)
    has any symbols has neighbors."""
    # calculate length and end column of number
    l = len(str(n))
    c_start = c
    c_end = c_start + l - 1
    # calculate neighboring coordinates and check if they are in
    # symbols
    for dr in [-1, 1]:
        for cc in range(c_start - 1, c_end + 2):
            rr = r + dr
            if (rr, cc) in symbols:
                # found a symbol, stop and return True
                return True

    # check for coordinates directly left and right
    for cc in [c_start - 1, c_end + 1]:
        if (r, cc) in symbols:
            return True

    return False


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # check that we have the correct number of numbers found
    # detect numbers with regex

    symbols, numbers = parse_grid_regex(puzzle_input)

    result = 0
    for n, r, c in numbers:
        # find neighbors of a number
        if has_symbol_neighbor(n, r, c, symbols):
            result += n

    return result


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/03.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 9:00 End: 11:10 (wrong end coordinate on numbers
#                                 at the end of the line)
# Part 2: Start:  End:
