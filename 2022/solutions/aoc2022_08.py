# Load any required modules. Most commonly used:

# import re
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
            puzzle_input.append(list(map(int, list(line.strip()))))

    return puzzle_input


def visible(grid, r, c) -> bool:
    """Return if a tree at given coordinates is visible from anywhere."""
    # row and column of the tree
    row = grid[r]
    col = [line[c] for line in grid]

    # height of the tree
    height = grid[r][c]
    # segments of row and col to left, right, top, bottom of tree
    left = row[:c]
    right = row[c + 1 :]
    top = col[:r]
    bottom = col[r + 1 :]

    # tree is visible if the highest tree on any side is lower than tree's height
    return any(max(side) < height for side in [left, right, top, bottom])


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # count trees on the side
    height = len(puzzle_input)
    width = len(puzzle_input[0])

    # count of visible trees (subtract 4 corners as double counted)
    count_visible = 2 * height + 2 * width - 4

    # count all visible trees in the middle
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            if visible(puzzle_input, r, c):
                count_visible += 1

    return count_visible


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/08.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 17:42 End: 18:04
# Part 2: Start: 18:05 End:
