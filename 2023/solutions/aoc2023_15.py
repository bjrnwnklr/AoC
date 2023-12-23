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
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    # Extract ints from the input
    #
    # signed ints
    # regex = re.compile(r"(-?\d+)")
    #
    # unsigned ints
    # regex = re.compile(r"(\d+)")
    #
    # with open(f_name, "r") as f:
    #     puzzle_input = []
    #     for line in f.readlines():
    #         matches = regex.findall(line.strip())
    #         if matches:
    #             puzzle_input.append(list(map(int, matches)))

    return puzzle_input


def hash_func(s):
    """Calculate the hash function of the provided string."""
    result = 0
    for c in list(s):
        result += ord(c)
        result *= 17
        result %= 256

    return result


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # split into individual steps
    parts = puzzle_input[0].strip().split(",")
    result = sum(hash_func(s) for s in parts)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    parts = puzzle_input[0].strip().split(",")
    boxes = defaultdict(list)
    for p in parts:
        # split into = and -
        if "=" in p:
            # = in part
            # get hashvalue and number
            label, focal = p.split("=")
            focal = int(focal)
            hv = hash_func(label)
            found = False
            for i, (l, f) in enumerate(boxes[hv]):
                if l == label:
                    boxes[hv].pop(i)
                    boxes[hv].insert(i, (label, focal))
                    found = True
                    break
            if not found:
                boxes[hv].append((label, focal))
        else:
            # - in part
            label = p.split("-")[0]
            hv = hash_func(label)
            for i, (l, f) in enumerate(boxes[hv]):
                if l == label:
                    boxes[hv].pop(i)
                    break

    # done processing, now calculate result
    result = 0
    for b in range(256):
        for i, (l, f) in enumerate(boxes[b]):
            result += (b + 1) * (i + 1) * f

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/15.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 14:11 End: 14:21
# Part 2: Start: 14:22 End: 14:59

# Elapsed time to run part1: 0.00525 seconds.
# Part 1: 501680
# Elapsed time to run part2: 0.00892 seconds.
# Part 2: 241094
