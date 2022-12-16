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
        for line in f.readlines():
            d, n = line.strip().split()
            puzzle_input.append((d, int(n)))

    return puzzle_input


@dataclass
class Knot:
    x: int = 0
    y: int = 0


DIRECTIONS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}


def move(direction, knot):
    """Move a knot one step into direction"""
    knot.x += direction[0]
    knot.y += direction[1]


def sign(n: int):
    """Return the sign of the number."""
    if n == 0:
        return 0
    elif n > 0:
        return 1
    else:
        return -1


def distance(head, tail):
    """Return the distance between head and tail for each
    coordinate."""
    return (head.x - tail.x, head.y - tail.y)


def one_move(direction, head, tail):
    """Move both head and tail by one step into direction."""
    # move the head
    move(DIRECTIONS[direction], head)
    # print(f"\tHead: {head}")

    # determine if tail needs to move
    # - if distance in x or y is > 2, tail needs to move
    # - tail moves by (sign(delta.x), sign(delta.y)),
    # i.e. if delta.x == 0: no move
    #      if delta.x > 0: move by 1
    #      if delta.x < 0: move by -1
    d = distance(head, tail)
    if abs(d[0]) > 1 or abs(d[1]) > 1:
        # move tail
        move((sign(d[0]), sign(d[1])), tail)
        # print(f"\tTail moved: {tail}")


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    How many positions does the tail of the rope visit at least once?
    This includes the starting position
    """
    tail_visits = set()
    head = Knot()
    tail = Knot()

    for direction, steps in puzzle_input:
        # print(f"Motion: {direction=}, {steps=}")
        for _ in range(steps):
            one_move(direction, head, tail)
            tail_visits.add((tail.x, tail.y))
            # print(f"\t{tail_visits=}")

    return len(tail_visits)


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/09.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 18:42 End: 19:08
# Part 2: Start: 19:09 End:
