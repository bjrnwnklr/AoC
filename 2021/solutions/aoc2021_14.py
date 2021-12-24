# Load any required modules. Most commonly used:

# import re
from collections import Counter, defaultdict
from utils.aoctools import aoc_timer


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


def process_polymer2(polydict, last_char, rules):
    d = defaultdict(int)
    char_counter = defaultdict(int)

    for k, v in polydict.items():
        new_poly_1 = k[0] + rules[k]
        new_poly_2 = rules[k] + k[1]
        char_counter[k[0]] += v
        char_counter[rules[k]] += v
        d[new_poly_1] += v
        d[new_poly_2] += v

    # add the last element - this never changes, it is simply the last character of the
    # overall starting template, so just needs to be added here once.
    # (We could also do this in the overall solution as it is only required once in the last
    # turn)
    char_counter[last_char] += 1
    return d, char_counter


@aoc_timer
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


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    poly_template, pair_rules = puzzle_input
    rules = {x: y for x, y in pair_rules}

    polydict = defaultdict(int)
    for pp in zip(poly_template[:], poly_template[1:]):
        pair = ''.join(pp)
        polydict[pair] += 1

    last_char = poly_template[-1]

    for _ in range(40):
        polydict, char_counter = process_polymer2(
            polydict.copy(), last_char, rules)

    # get the max and min occurence
    c_min = min(char_counter.values())
    c_max = max(char_counter.values())

    return c_max - c_min


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/14.txt')
    # puzzle_input = load_input('testinput/14_1_1.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 11:15 End: 11:41
# Part 2: Start: 11:42 End: 12:41

# Elapsed time to run part1: 0.00469 seconds.
# Part 1: 2602
# Elapsed time to run part2: 0.00219 seconds.
# Part 2: 2942885922173
