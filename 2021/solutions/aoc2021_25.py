# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def parse_map(puzzle_input: list[str]) -> tuple[set[tuple[int, int]]]:
    """Parse the puzzle input map and generate two sets of coordinates, one for 
    east facing cucumbers, one for south facings cucumbers.

    Returns (east, south) sets of cucumbers and the number of rows and columns.
    """
    rows = len(puzzle_input)
    cols = len(puzzle_input[0])
    east = set()
    south = set()
    for r in range(rows):
        for c in range(cols):
            match puzzle_input[r][c]:
                case 'v':
                    south.add((r, c))
                case '>':
                    east.add((r, c))

    return east, south, rows, cols


def move(cuc_to_move: set[tuple[int, int]], other_cucs: set[tuple[int, int]], direction: tuple[int, int], rows: int, cols: int) -> tuple[bool, set[tuple[int, int]]]:
    """Process a herd of cucumbers' moves in the given direction.

    Returns:
    - True if any of the herd moved, False if none moved.
    - An updated set of cucumber coordinates.
    """
    moved_cucumbers = set()
    moved = False
    all_cucumbers = cuc_to_move | other_cucs
    for r, c in cuc_to_move:
        rr = (r + direction[0]) % rows
        cc = (c + direction[1]) % cols
        if (rr, cc) not in all_cucumbers:
            moved_cucumbers.add((rr, cc))
            moved = True
        else:
            moved_cucumbers.add((r, c))

    return moved, moved_cucumbers


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    east, south, rows, cols = parse_map(puzzle_input)
    steps = 0
    moved = True
    while moved:
        moved_east, east = move(east, south, (0, 1), rows, cols)
        moved_south, south = move(south, east, (1, 0), rows, cols)
        moved = moved_east or moved_south
        steps += 1

    return steps


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/25.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')


# Part 1: Start: 16:45 End: 17:27

# Elapsed time to run part1: 1.43875 seconds.
# Part 1: 417
