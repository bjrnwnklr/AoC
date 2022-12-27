# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer
from dataclasses import dataclass


@dataclass
class Node:
    x: int = 500
    y: int = 0

    def __hash__(self) -> int:
        return self.x * 10_000 + self.y


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            segments = line.strip().split(" -> ")
            sublist = []
            for s in segments:
                sublist.append(tuple(map(int, s.split(","))))
            puzzle_input.append(sublist)

    return puzzle_input


def generate_walls(puzzle_input):
    walls = set()
    for line in puzzle_input:
        for i in range(len(line) - 1):
            x1, y1 = line[i]
            x2, y2 = line[i + 1]
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    walls.add(Node(x1, y))
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    walls.add(Node(x, y1))
            else:
                raise ValueError(
                    f"x and y coordinates differ in both places: {x1=} {y1=} {x2=} {y2=}"
                )

    return walls


def fall(s: Node, walls, sand, abyss):
    """Simulates a falling grain of sand.

    Return True if sand comes to rest, or false if it drops into
    the abyss.
    """
    while s.y < abyss:
        s_down = Node(s.x, s.y + 1)
        s_down_left = Node(s.x - 1, s.y + 1)
        s_down_right = Node(s.x + 1, s.y + 1)
        if s_down not in walls and s_down not in sand:
            s.y += 1
        elif s_down_left not in walls and s_down_left not in sand:
            s.x -= 1
            s.y += 1
        elif s_down_right not in walls and s_down_right not in sand:
            s.x += 1
            s.y += 1
        elif s.x == 500 and s.y == 0:
            # part 2 - sand comes to rest at source
            sand.add(s)
            return False
        else:
            # sand comes to rest
            sand.add(s)
            return True

    # if we get here, and is falling into the abyss
    return False


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    walls = generate_walls(puzzle_input)

    # determine lower boundary (the abyss)
    min_wall = max(walls, key=lambda n: n.y)
    abyss = min_wall.y + 1

    # track if the sand stabilizes (i.e. falls into the abyss)
    falling = True
    # set of grains
    sand = set()
    while falling:
        # generate a new grain of sand
        # drop sand downwards until it stops or falls to the abyss
        s = Node()
        falling = fall(s, walls, sand, abyss)

    return len(sand)


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    Simulate with floor infinite at lowest y point + 2 (11 = 9 + 2 in example.)

    At what point does the source at (500, 0) fill up?
    i.e. when does a grain come to rest at (500, 0)?
    """
    walls = generate_walls(puzzle_input)

    # determine lower boundary (the abyss)
    min_wall = max(walls, key=lambda n: n.y)
    abyss = min_wall.y + 3

    # add bottom to walls
    x_span = 10_000
    for x in range(-x_span, x_span):
        walls.add(Node(x, abyss - 1))

    # track if the sand stabilizes (i.e. falls into the abyss)
    falling = True
    # set of grains
    sand = set()
    while falling:
        # generate a new grain of sand
        # drop sand downwards until it stops or falls to the abyss
        s = Node()
        falling = fall(s, walls, sand, abyss)

    return len(sand)


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/14.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start:  End:
# Part 2: Start:  End:

# Elapsed time to run part1: 0.20075 seconds.
# Part 1: 1068
# Elapsed time to run part2: 5.63967 seconds.
# Part 2: 27936
