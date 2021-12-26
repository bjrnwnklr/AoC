# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer


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


def add(a, b):
    """Add two snailfish numbers a and b to each other and return the added number."""
    return [a, b]


def convert(sn):
    """Convert a snailfish number from a string to a list with integers."""
    return eval(sn)


def reduce(sn):
    """Reduce a snailfish number until no further reduction is possible.

    To reduce a snailfish number, you must repeatedly do the first action
    in this list that applies to the snailfish number:

    - If any pair is nested inside four pairs, the leftmost such pair explodes.
    - If any regular number is 10 or greater, the leftmost such regular number splits.
    """
    changed = True
    while changed:
        changed = False
        # parse from the left and count opening paranthesis and check for any numbers > 10
        new_sn = []
        open_par_count = 0
        # last integer encountered, position encountered
        last_int_left = (None, None)

    return ''

# @aoc_timer


def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    return 1


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/18.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 18:05 End:
# Part 2: Start:  End:
