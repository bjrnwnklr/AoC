# Load any required modules. Most commonly used:

# import re
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

    return puzzle_input


def parse_grid(puzzle_input):
    """Parse the puzzle input into a grid."""
    grid = []
    for row in puzzle_input:
        grid.append([x for x in list(row)])
    return grid


DIRS = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}  # rigth  # down  # left  # up
SPLIT = {"|": [3, 1], "-": [0, 2]}
MIRROR = {
    ("\\", 0): 1,
    ("\\", 1): 0,
    ("\\", 2): 3,
    ("\\", 3): 2,
    ("/", 0): 3,
    ("/", 1): 2,
    ("/", 2): 1,
    ("/", 3): 0,
}


def print_grid(grid, energized):
    """Print the grid"""
    for r, row in enumerate(grid):
        line = ""
        for c, g in enumerate(row):
            line += "#" if (r, c) in energized else g
        print(line)
    print()


def energize_grid(grid, start):
    """Energize the grid and return number of energized cells.
    Start from the provided start (position, direction)."""
    height = len(grid)
    width = len(grid[0])
    energized = set()  # set of energized cells
    seen = set()
    # stop when the number of energized cells does not change between steps
    beams = [start]
    while beams:
        b, d = beams.pop(0)
        # check if new beam is within grid
        if not (0 <= b[0] < height) or not (0 <= b[1] < width):
            continue

        # add the current cell of the beam to the set
        # of energized cells if not already in it
        if (b, d) in seen:
            continue

        energized.add(b)
        seen.add((b, d))

        # assess where beam is
        g = grid[b[0]][b[1]]
        moves = []
        if g == ".":
            # on stone, just continue in current direction
            moves.append((DIRS[d], d))
        elif g == "-":
            # if hitting from left or right, just continue
            if d in [0, 2]:
                moves.append((DIRS[d], d))
            else:
                # split
                for new_d in SPLIT[g]:
                    moves.append((DIRS[new_d], new_d))
        elif g == "|":
            if d in [1, 3]:
                moves.append((DIRS[d], d))
            else:
                # split
                for new_d in SPLIT[g]:
                    moves.append((DIRS[new_d], new_d))
        else:
            # must be a mirror \ or /
            new_d = MIRROR[(g, d)]
            moves.append((DIRS[new_d], new_d))

        for (dr, dc), d in moves:
            beams.append(((b[0] + DIRS[d][0], b[1] + DIRS[d][1]), d))

    return len(energized)


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    grid = parse_grid(puzzle_input)
    result = energize_grid(grid, ((0, 0), 0))

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    grid = parse_grid(puzzle_input)

    height = len(grid)
    width = len(grid[0])
    starting_pos = []
    for r in range(height):
        starting_pos.append(((r, 0), 0))
        starting_pos.append(((r, width - 1), 2))
    for c in range(width):
        starting_pos.append(((0, c), 1))
        starting_pos.append(((height - 1, c), 3))

    max_energized = 0
    for s in starting_pos:
        max_energized = max(max_energized, energize_grid(grid, s))

    return max_energized


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/16.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 15:28 End: 17:19 (with break)
# Part 2: Start: 17:20 End: 17:36

# Elapsed time to run part1: 0.01077 seconds.
# Part 1: 8389
# Elapsed time to run part2: 2.43982 seconds.
# Part 2: 8564
