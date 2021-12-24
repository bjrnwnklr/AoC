# Load any required modules. Most commonly used:

# import re
from collections import Counter
# from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:

        top, bottom = f.read().strip().split('\n\n')

        poly_template = top.strip()

        puzzle_input = []
        for line in bottom.split('\n'):
            puzzle_input.append(line.strip().split(' -> '))

    return (poly_template, puzzle_input)


def process_polymer(poly, rules):
    new_poly = ''
    for pp in zip(poly[:], poly[1:]):
        pair = ''.join(pp)
        # only add the first element and then the new element, otherwise we
        # would duplicate each middle element (as it is the 2nd of the first pair and
        # the 1st of the second pair)
        new_poly += pp[0] + rules[pair]

    # add the last element as we don't add it in the iteration
    new_poly += poly[-1]

    return new_poly
# @aoc_timer


def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    What do you get if you take the quantity of the most 
    common element and subtract the quantity of the least common element?
    """

    poly_template, pair_rules = puzzle_input
    rules = {x: y for x, y in pair_rules}

    new_poly = poly_template
    for _ in range(10):
        new_poly = process_polymer(new_poly, rules)

    # count the elements
    c = Counter(new_poly)

    return c.most_common()[0][1] - c.most_common()[-1][1]


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/14.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 11:15 End: 11:41
# Part 2: Start: 11:42 End:
