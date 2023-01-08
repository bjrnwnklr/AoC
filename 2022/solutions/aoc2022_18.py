# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer
from dataclasses import dataclass

sides = [
    (-1, 0, 0),  # x left
    (1, 0, 0),  # x right
    (0, -1, 0),  # y left
    (0, 1, 0),  # y right
    (0, 0, -1),  # z left
    (0, 0, 1),  # z right
]


@dataclass
class Cube:
    x: int
    y: int
    z: int
    sides: int = 6

    def coords(self):
        """Return tuple of (x, y, z) coordinates"""
        return (self.x, self.y, self.z)

    def adjacent(self, s: tuple[int]) -> tuple[int]:
        """Return the coordinates of an adjacent side"""
        return (self.x + s[0], self.y + s[1], self.z + s[2])


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(list(map(int, line.strip().split(","))))

    return puzzle_input


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    cubes = [Cube(x, y, z) for x, y, z in puzzle_input]

    # generate set of all cube coordinates
    coords = set(cube.coords() for cube in cubes)

    # iterate through cubes and decrease count of sides
    # if a side is found in the coordinates of all cubes
    for cube in cubes:
        for s in sides:
            adj_cube = cube.adjacent(s)
            if adj_cube in coords:
                cube.sides -= 1
                assert cube.sides >= 0

    return sum(cube.sides for cube in cubes)


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/18.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 17:30 End: 18:00
# Part 2: Start: 18:01 End:
