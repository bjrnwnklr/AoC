# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer
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


def move_tail(head, tail):
    """Move tail by one step into direction."""
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


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    How many positions does the tail of the rope visit at least once?
    This includes the starting position
    """
    tail_visits = set()
    head = Knot()
    tail = Knot()

    for direction, steps in puzzle_input:
        for _ in range(steps):
            move(DIRECTIONS[direction], head)
            move_tail(head, tail)
            tail_visits.add((tail.x, tail.y))

    return len(tail_visits)


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    Rope is now 10 knots long (head, 8 middle, tail)

    How many positions does the tail of the rope visit at least once?
    This includes the starting position
    """
    tail_visits = set()
    knots = [Knot() for _ in range(10)]

    for direction, steps in puzzle_input:
        for _ in range(steps):
            # move head - always moves
            move(DIRECTIONS[direction], knots[0])
            for i in range(9):
                # move the other knots
                move_tail(knots[i], knots[i + 1])
            tail_visits.add((knots[9].x, knots[9].y))

    return len(tail_visits)


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
# Part 2: Start: 19:09 End: 19:29

# Elapsed time to run part1: 0.01072 seconds.
# Part 1: 6081
# Elapsed time to run part2: 0.04979 seconds.
# Part 2: 2487
