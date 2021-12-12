# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer

ERROR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

MATCHING_PARA = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

COMPLETE_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


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


def parse_corrupt(line_str):
    """Parse opening parantheses and abort if mismatch in closing parantheses is found."""
    stack = []
    line = list(line_str)
    while line:
        c = line.pop(0)
        if c in MATCHING_PARA:
            # opening parathensis, push on stack
            stack.append(c)
        else:
            # closing paranthesis, we should have a matching opening on the stack
            o = stack.pop()
            if MATCHING_PARA[o] != c:
                return True, c

    return False, None


def parse_incomplete(line_str):
    """Parse opening parantheses and calculate the autocomplete score. Discard corrupted lines."""
    stack = []
    line = list(line_str)
    while line:
        c = line.pop(0)
        if c in MATCHING_PARA:
            # opening parathensis, push on stack
            stack.append(c)
        else:
            # closing paranthesis, we should have a matching opening on the stack
            # Assert that we really find a matching paranthesis!
            o = stack.pop()
            assert MATCHING_PARA[o] == c

    # now work through the remaining stack and autocomplete
    result = 0
    while stack:
        o = stack.pop()
        result *= 5
        result += COMPLETE_SCORE[MATCHING_PARA[o]]

    return result


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    result = 0
    for line in puzzle_input:
        status, e = parse_corrupt(line)
        if status:
            result += ERROR_SCORE[e]

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    # find the incomplete lines using part 1
    incomplete_lines = []
    for line in puzzle_input:
        status, _ = parse_corrupt(line)
        if not status:
            incomplete_lines.append(line)

    # now parse the incomplete lines only
    results = []
    for line in incomplete_lines:
        results.append(parse_incomplete(line))

    # find the middle one
    middle_index = int(len(results) / 2)
    middle_score = sorted(results)[middle_index]

    return middle_score


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/10.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 13:55 End: 14:17
# Part 2: Start: 14:18 End: 14:35
