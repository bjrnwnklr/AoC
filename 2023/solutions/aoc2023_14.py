# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
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

    return puzzle_input


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    grid = [[x for x in row] for row in puzzle_input]
    north_tilt = [["#" if x == "#" else "." for x in row] for row in puzzle_input]

    # height of the grid
    height = len(grid)

    result = 0
    for r, row in enumerate(grid):
        for c, x in enumerate(row):
            # move each round rock up as much as possible
            if grid[r][c] == "O":
                # look north to find next free slot on north_tilt grid
                dr = 1
                while r - dr >= 0:
                    if north_tilt[r - dr][c] == ".":
                        dr += 1
                    else:
                        break
                north_tilt[r - dr + 1][c] = "O"
                result += height - (r - dr + 1)

    return result


def rotate_grid(grid):
    """Rotate the grid clockwise by 90 degrees"""
    rotated = []
    for c in range(len(grid[0])):
        line = []
        for r in range(len(grid) - 1, -1, -1):
            line.append(grid[r][c])
        rotated.append(line)

    return rotated


def hash_grid(grid):
    """Generate a simple hash from the grid:
    Create a string representation of the grid."""
    hashstring = ""
    for line in grid:
        hashstring += "".join(line)
    return hashstring


def calc_weight(grid):
    """Calculate the weight of the grid"""
    height = len(grid)
    weight = 0
    for r, row in enumerate(grid):
        weight += row.count("O") * (height - r)

    return weight


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    cycles = 1_000_000_000
    # run for 1bn cycles - check if there is a repeating pattern of weights
    # at some point

    # rotate the grid clockwise 4 times each cycle
    grid = [[x for x in row] for row in puzzle_input]

    # store the results of the cycles to see if we find a repeating pattern
    cycle_results = dict()
    same_results = defaultdict(list)

    for i in range(1, cycles + 1):
        for _ in range(4):
            north_tilt = [["#" if x == "#" else "." for x in row] for row in grid]
            for r, row in enumerate(grid):
                for c, x in enumerate(row):
                    # move each round rock up as much as possible
                    if grid[r][c] == "O":
                        # look north to find next free slot on north_tilt grid
                        dr = 1
                        while r - dr >= 0:
                            if north_tilt[r - dr][c] == ".":
                                dr += 1
                            else:
                                break
                        north_tilt[r - dr + 1][c] = "O"
            # rotate grid
            grid = rotate_grid(north_tilt)
        # store result after turning 4 clockwise turns
        weight = calc_weight(grid)
        cycle_results[i] = weight
        hg = hash_grid(grid)
        same_results[hg].append(i)
        if len(same_results[hg]) > 30:
            print(
                f"Found potential repeating pattern: Cycles: {same_results[hg]}, result: {weight}"
            )
            break

    # calculate periodicity and then the result
    periodicity = []
    for pattern in same_results:
        if len(same_results[pattern]) > 20:
            periodicity.append(same_results[pattern][1] - same_results[pattern][0])
    if len(set(periodicity)) == 1:
        # all results have the same periodicity
        p = periodicity[0]
        print(f"Same periodicity: {p}")
        # calculate offset / remainder for the number of cycles
        offsets = [
            same_results[pattern][0]
            for pattern in same_results
            if len(same_results[pattern]) > 20
        ]
        print(f"{offsets=}")
        for o in offsets:
            if ((cycles - o) % p) == 0:
                print(f"Found solution: {o}, {cycle_results[o]}")
                result = cycle_results[o]
    else:
        print(f"No same periodicity found: {periodicity}")
        result = -1

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/14.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 16:46 End: 17:18
# Part 2: Start: 17:19 End: 18:45

# Elapsed time to run part1: 0.00138 seconds.
# Part 1: 109755
# Elapsed time to run part2: 4.90607 seconds.
# Part 2: 90928
