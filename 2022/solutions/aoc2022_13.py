# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer
from dataclasses import dataclass


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


@dataclass
class Packet:
    payload: list

    def __lt__(self, other):
        return compare(self.payload, other.payload) == 1


def compare(left, right):
    print(f"Compare {left} vs {right}")
    result = 0
    while left and right and result == 0:
        l = left.pop(0)
        r = right.pop(0)
        # check what type left and right are
        if isinstance(l, int) and isinstance(r, int):
            # atomic case, if left is smaller than right list is valid
            if l < r:
                result = 1
            elif l > r:
                result = -1
        elif isinstance(l, list) and isinstance(r, list):
            result = compare(l, r)
        else:
            if isinstance(l, int):
                result = compare([l], r)
            elif isinstance(r, int):
                result = compare(l, [r])

    # if one of the checks produced a result, we have a result
    if result != 0:
        return result
    elif not left and not right:
        # both lists empty, left and right were equal
        return 0
    else:
        # check if one of the lists ran out early
        if len(left) < len(right):
            # left ran out early
            return 1
        elif len(left) > len(right):
            # right ran out early
            return -1


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    score = 0
    for i, (left, right) in enumerate(puzzle_input, start=1):
        result = compare(left, right)
        if result == 1:
            score += i

    return score


# @aoc_timer
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
    p1 = sorted_packets.index(Packet([[2]]))
    p2 = sorted_packets.index(Packet([[6]]))

    return (p1 + 1) * (p2 + 1)


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
# Part 2: Start: 10:00 End:
