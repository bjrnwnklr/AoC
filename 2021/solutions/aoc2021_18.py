# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer
import math


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
    return f'[{a},{b}]'


def to_str(sn_list):
    """Convert a snailfish list to a string representation"""
    return ''.join(str(c) for c in sn_list)


def tokenize(sn_string):
    """Tokenize a snailfish number from a string to a list with integers."""
    result = []
    i = ''
    s = list(sn_string)
    while s:
        c = s.pop(0)
        if c == '[':
            result.append(c)
        elif c in [']', ',']:
            if i != '':
                result.append(int(i))
                i = ''
            result.append(c)
        else:
            # must be a number
            i += c

    return result


def explode(sn_str):
    """Process one explosion by parsing the tokens 
    - counting parantheses depth
    - if a depth >= 5 found, process explosion by searching left and right for
      integers to add to
    - Return a completed number, converted back to a string
    """
    # Tokenize - convert from string to list of tokens as it is easier to process
    sn = tokenize(sn_str)

    i = 0
    depth = 0
    while i < len(sn):
        c = sn[i]
        if c == '[':
            depth += 1
            if depth == 5:
                # explode
                left_num = sn[i + 1]
                right_num = sn[i + 3]
                # snippets to the left and right of the numbers
                left = sn[:i]
                right = sn[i + 5:]
                # print(f'Explode (pre):  {convert_snlist_to_str(sn)=}')
                # look for the last integer in the left list
                for j in range(len(left) - 1, -1, -1):
                    if isinstance(left[j], int):
                        left[j] += left_num
                        break
                # look for the next integer in the right list
                for j in range(len(right)):
                    if isinstance(right[j], int):
                        right[j] += right_num
                        break
                # now put the left and right elements together with a 0 in the middle
                sn = left + [0] + right
                # print(f'Explode (post): {convert_snlist_to_str(sn)=}')
                # print()
                break
            else:
                i += 1
        elif c == ']':
            depth -= 1
            i += 1
        else:
            i += 1

    # convert resulting snailfish number back to a string as it is easier to compare to each other
    return to_str(sn)


def split_sn(sn_str):
    """Perform one split operation on the snailfish number string."""
    # Tokenize - convert from string to list of tokens as it is easier to process
    sn = tokenize(sn_str)

    i = 0
    while i < len(sn):
        c = sn[i]
        if isinstance(c, int):
            if c >= 10:
                # split
                # snippets to the left and the right of the number to be split
                left = sn[:i]
                right = sn[i + 1:]
                # left number gets rounded down, right number gets rounded up
                left_num = math.floor(c / 2)
                right_num = math.ceil(c / 2)
                # print(f'Split (post):   {convert_snlist_to_str(sn)=}')
                # replace the split number with the new pair and bracket in between the
                # left and right snippets
                sn = left + ['[', left_num, ',', right_num, ']'] + right
                # print(f'Split (pre):    {convert_snlist_to_str(sn)=}')
                # print()
                break
            else:
                i += 1
        else:
            i += 1

    # convert resulting snailfish number back to a string as it is easier to compare to each other
    return to_str(sn)


def reduce(sn):
    """Reduce a snailfish number until no further reduction is possible.

    To reduce a snailfish number, you must repeatedly do the first action
    in this list that applies to the snailfish number:

    - If any pair is nested inside four pairs, the leftmost such pair explodes.
    - If any regular number is 10 or greater, the leftmost such regular number splits.
    """
    changed = True
    sn_post_split = sn
    while changed:
        changed = False
        # Run explode as many times as required - until no further pairs to explode
        sn_pre_explode = sn_post_split
        sn_post_explode = explode(sn_pre_explode)
        while sn_pre_explode != sn_post_explode:
            changed = True
            sn_pre_explode = sn_post_explode
            sn_post_explode = explode((sn_pre_explode))

        # do a single split once no further explosions possibly
        sn_pre_split = sn_post_explode
        sn_post_split = split_sn(sn_pre_split)
        if sn_pre_split != sn_post_split:
            changed = True

    return sn_post_split


def add_all_numbers(puzzle_input):
    """Process all numbers in the input and add them up."""
    current_number = puzzle_input.pop(0)
    while puzzle_input:
        next_number = puzzle_input.pop(0)
        temp_number = add(current_number, next_number)
        current_number = reduce(temp_number)

    return current_number


def magnitude(sn_list):
    """Recursively calculate the magnitude of a snailfish number (which needs to be in
    a python list format with integers).
    """
    if isinstance(sn_list, int):
        return sn_list
    else:
        return 3 * magnitude(sn_list[0]) + 2 * magnitude(sn_list[1])


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    added_number = add_all_numbers(puzzle_input)
    # turn the resulting number into a python list
    sn_list = eval(added_number)

    return magnitude(sn_list)


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

# Part 1: Start: 18:05 End: 11:17 (next day, worked until 22:00 previous night)
# Part 2: Start: 11:18 End:
