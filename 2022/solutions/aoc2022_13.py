# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer
from dataclasses import dataclass
from copy import deepcopy
from ast import literal_eval


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
            puzzle_input.append((literal_eval(left), literal_eval(right)))

    return puzzle_input


@dataclass
class Packet:
    payload: list

    def __lt__(self, other):
        return compare(self.payload, other.payload) == -1


def compare(left, right):
    """Compare left and right list according to rules.
    Return
    - -1 if left is smaller (in correct order) than right
    - 1 if right is smaller (not in correct order) than left
    - 0 if left and right are equal
    """
    if isinstance(left, int) and isinstance(right, int):
        # atomic case, if left is smaller than right list is valid
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0
    elif isinstance(left, list) and isinstance(right, list):
        # both are lists, compare elements one by one
        i = 0
        result = 0
        while i < min(len(left), len(right)):
            result = compare(left[i], right[i])
            if result != 0:
                return result
            i += 1

        # if we get here, one or both lists ran out without finding
        # a result. Check which list ran out
        if len(left) == i and len(right) > i:
            # left list ran out first
            return -1
        elif len(right) == i and len(left) > i:
            return 1
        else:
            # both lists have the same length - equal
            return 0
    else:
        # one element is an int, the other a list
        # convert int to list and compare
        if isinstance(left, int):
            return compare([left], right)
        elif isinstance(right, int):
            return compare(left, [right])


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    score = 0
    for i, (left, right) in enumerate(puzzle_input, start=1):
        result = compare(left, right)
        if result == -1:
            score += i

    return score


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    - add [[2]] and [[6]]
    - put all packets into the right order, including the two new ones
    - multiply the index of the new packets (starting at index 1) for the result

    Implement using the `__lt__` comparison and then sort the list using `sorted`
    """
    # create one list of all packets
    packets = []
    for left, right in puzzle_input:
        packets.append(Packet(left))
        packets.append(Packet(right))

    # add two new packets
    packets.append(Packet([[2]]))
    packets.append(Packet([[6]]))

    # sort list
    sorted_packets = sorted(packets)

    # find indices of the two packets
    p1 = sorted_packets.index(Packet([[2]])) + 1
    p2 = sorted_packets.index(Packet([[6]])) + 1

    return p1 * p2


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/13.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    puzzle_input = load_input("input/13.txt")
    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 16:15 End: 17:35
# Part 2: Start: 10:00 End:

# Elapsed time to run part1: 0.00068 seconds.
# Part 1: 6415
# Elapsed time to run part2: 0.01076 seconds.
# Part 2: 20056
