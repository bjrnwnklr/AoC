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
        blocks = f.read().split("\n\n")
        for block in blocks:
            left, right = block.strip().split("\n")
            puzzle_input.append((eval(left), eval(right)))

    return puzzle_input


def compare(left, right):
    print(f"Compare {left} vs {right}")
    result = 0
    while left and right and result == 0:
        l = left.pop(0)
        r = right.pop(0)
        print(f"Compare {l} vs {r}")
        # check what type left and right are
        if isinstance(l, int) and isinstance(r, int):
            # atomic case, if left is smaller than right list is valid
            # print("Both integers")
            if l < r:
                print("Left side is smaller - correct")
                result = 1
            elif l > r:
                print("Right side is smaller - not correct")
                result = -1
        elif isinstance(l, list) and isinstance(r, list):
            # print("Both lists")
            result = compare(l, r)
        else:
            if isinstance(l, int):
                # print("l is int", type(l), type(r))
                result = compare([l], r)
            elif isinstance(r, int):
                # print("r is integer", type(l), type(r))
                result = compare(l, [r])

    # print(f"Loop completed. {result=}, {left=}, {right=}")
    if result != 0:
        return result
    elif not left and not right:
        # both lists empty
        return 0
    else:
        # check if one of the lists ran out early
        if len(left) < len(right):
            print("Left side ran out of items - correct")
            return 1
        elif len(left) > len(right):
            print("Right side ran out of items - not correct")
            return -1


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    score = 0
    for i, (left, right) in enumerate(puzzle_input, start=1):
        print(f"Pair {i}: {left} {right}")
        result = compare(left, right)
        if result == 1:
            score += i

    return score


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/13.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 16:15 End: 17:35
# Part 2: Start: 17:36 End:
