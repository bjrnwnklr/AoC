# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from itertools import combinations
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


def parse_grid(puzzle_input, factor):
    """Parse the grid into a dictionary of galaxies,
    compensating for any rows or columns without any galaxies."""
    # first scan into a grid
    grid = []
    for row in puzzle_input:
        grid.append(list(row))

    # scan through columns and identify empty columns
    empty_cols = []
    for c in range(len(grid[0])):
        if all(grid[r][c] == "." for r in range(len(grid))):
            empty_cols.append(c)

    # scan through rows and identify empty rows
    empty_rows = []
    for r in range(len(grid)):
        if all(grid[r][c] == "." for c in range(len(grid[r]))):
            empty_rows.append(r)

    # generate coordinates of galaxies, but adjusted for the
    # double rows / columns
    galaxies = set()
    rr = 0
    for r, row in enumerate(grid):
        if r in empty_rows:
            rr += factor
            # no need to scan through row as it is empty
            continue
        cc = 0
        for c, col in enumerate(row):
            if c in empty_cols:
                cc += factor
                # no need to evaluate the current cell as it is
                # empty anyway, continue with next columns
                continue
            if col == "#":
                # found a galaxy, store the location
                galaxies.add((r + rr, c + cc))

    return galaxies


def manhattan_distance(a, b):
    """Calculate the Manhattan distance between two coordinates."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    galaxies = parse_grid(puzzle_input, 1)

    # go through combinations of the galaxies and calculate the
    # sum of the distance
    result = sum(manhattan_distance(a, b) for a, b in combinations(galaxies, 2))

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # add 999_999 rows for each empty row or column (to get to 1_000_000)
    galaxies = parse_grid(puzzle_input, 999_999)

    # go through combinations of the galaxies and calculate the
    # sum of the distance
    result = sum(manhattan_distance(a, b) for a, b in combinations(galaxies, 2))

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/11.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 11:23  End: 11:53
# Part 2: Start: 11:54 End: 11:57 (+1 error initially...)

# Elapsed time to run part1: 0.01395 seconds.
# Part 1: 9565386
# Elapsed time to run part2: 0.01566 seconds.
# Part 2: 857986849428
