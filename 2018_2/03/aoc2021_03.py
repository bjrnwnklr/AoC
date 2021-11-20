# Load any required modules. Most commonly used:

import re
from collections import defaultdict


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
        regex = re.compile(r'(\d+)')
        for line in f.readlines():
            coords = list(map(int, regex.findall(line.strip())))
            puzzle_input.append(coords)

    return puzzle_input


def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    Args:
        puzzle_input (List): Typically a list of the input values from the input.txt puzzle input.

    Returns:
        Depends...: Typically an Integer value, but often also a String - this can be used on adventofcode 
        as the answer to the puzzle.
    """
    grid = defaultdict(int)

    for _, x, y, width, height in puzzle_input:
        for dx in range(width):
            for dy in range(height):
                grid[(x + dx, y + dy)] += 1

    return sum(1 for c in grid if grid[c] > 1)


def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    Args:
        puzzle_input (List): Typically a list of the input values from the input.txt puzzle input.

    Returns:
        Depends...: Typically an Integer value, but often also a String - this can be used on adventofcode 
        as the answer to the puzzle.
    """
    grid = defaultdict(list)
    not_overlapping = set()

    for i, x, y, width, height in puzzle_input:
        not_overlapping.add(i)
        for dx in range(width):
            for dy in range(height):
                g = grid[(x + dx, y + dy)]
                g.append(i)
                if len(g) > 1:
                    for j in g:
                        if j in not_overlapping:
                            not_overlapping.remove(j)

    return list(not_overlapping)[0]


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')
