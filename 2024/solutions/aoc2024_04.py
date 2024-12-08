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
        puzzle_input = defaultdict(str)
        for r, line in enumerate(f.readlines()):
            for c, letter in enumerate(list(line.strip())):
                puzzle_input[(r, c)] = letter

    return puzzle_input


n_coords = [
    [(0, 1), (0, 2), (0, 3)],  # right horizontal
    [(1, 0), (2, 0), (3, 0)],  # down vertical
    [(0, -1), (0, -2), (0, -3)],  # left horizontal
    [(-1, 0), (-2, 0), (-3, 0)],  # up vertical
    [(-1, 1), (-2, 2), (-3, 3)],  # up right
    [(1, 1), (2, 2), (3, 3)],  # down right
    [(1, -1), (2, -2), (3, -3)],  # down left
    [(-1, -1), (-2, -2), (-3, -3)],  # up left
]

x_coords = [
    [(-1, -1), (0, 0), (1, 1)],  # top left to bottom right
    [(1, -1), (0, 0), (-1, 1)],  # bottom left to top right
]


def get_neighbors(r, c, r_max, c_max, coords):
    """Get the neighboring 3 coordinates for a coordinate in
    row, column pair format.

    Neighbors are 3 upwards, 3 downwards, 3 left, 3 right,
    3 diagonal in each direction."""
    # stop if we are leaving the boundaries
    neighbors = []
    for dx in coords:
        neighbor = []
        in_bounds = True
        for dr, dc in dx:
            rr = dr + r
            cc = dc + c
            if 0 <= rr <= r_max and 0 <= cc <= c_max:
                neighbor.append((rr, cc))
            else:
                in_bounds = False
                break
                # one of the neighbors is out of bounds,
                # stop and discard and go to the next
                # neighbor check
        if in_bounds:
            neighbors.append(neighbor)
    return neighbors


def get_word(grid, coords):
    """Return the letters formed by the coordinates
    given."""
    word = "".join(grid[(r, c)] for r, c in coords)
    return word


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # get boundaries of the grid
    r_max = max(r[0] for r in puzzle_input.keys())
    c_max = max(r[1] for r in puzzle_input.keys())

    # iterate through each coordinate, get neighbors
    # and check if the neighbors spell XMAS
    WORD = "XMAS"
    result = 0
    for r in range(r_max + 1):
        for c in range(c_max + 1):
            # check if the letter is an X
            if puzzle_input[(r, c)] == WORD[0]:
                neighbors = get_neighbors(r, c, r_max, c_max, n_coords)
                for neighbor in neighbors:
                    word_coords = [(r, c)]
                    word_coords.extend(neighbor)
                    word = get_word(puzzle_input, word_coords)
                    if word == WORD:
                        # we found a match
                        result += 1

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # get boundaries of the grid
    r_max = max(r[0] for r in puzzle_input.keys())
    c_max = max(r[1] for r in puzzle_input.keys())

    # iterate through each coordinate, get neighbors
    # and check if the neighbors spell MAS
    WORD = "MAS"
    result = 0
    for r in range(r_max + 1):
        for c in range(c_max + 1):
            # check if the letter is an A
            if puzzle_input[(r, c)] == WORD[1]:
                neighbors = get_neighbors(r, c, r_max, c_max, x_coords)
                matches = 0
                for neighbor in neighbors:
                    word_coords = neighbor[:]
                    word = get_word(puzzle_input, word_coords)
                    if word == WORD or word == WORD[::-1]:
                        # we found a match
                        matches += 1
                if matches == 2:
                    result += 1
    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/04.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 11:58 End: 12:41
# Part 2: Start: 13:40 End: 13:53

# Elapsed time to run part1: 0.04089 seconds.
# Part 1: 2571
# Elapsed time to run part2: 0.01764 seconds.
# Part 2: 1992
