# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer
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


@aoc_timer
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


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    Use flood fill to find reachable pockets within the
    cube and outside (draw a +1 perimeter outside on each side).
    """
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

    total_sides = sum(cube.sides for cube in cubes)

    # generate a +1 cube around the cluster, but
    # exclude the coordinates of the actual cubes
    min_x = min(cube.x for cube in cubes) - 1
    min_y = min(cube.y for cube in cubes) - 1
    min_z = min(cube.z for cube in cubes) - 1
    max_x = max(cube.x for cube in cubes) + 1
    max_y = max(cube.y for cube in cubes) + 1
    max_z = max(cube.z for cube in cubes) + 1

    perimeter_cube = set(
        (x, y, z)
        for x in range(min_x, max_x + 1)
        for y in range(min_y, max_y + 1)
        for z in range(min_z, max_z + 1)
        if (x, y, z) not in coords
    )

    # BFS / Flood Fill the coordinates of the perimeter cube
    # Anything remaining in perimeter_cube are trapped cubes
    # not reachable from outside
    # start in bottom left corner of the perimeter
    q = [(min_x, min_y, min_z)]

    while q:
        curr_cube = q.pop(0)

        if curr_cube not in perimeter_cube:
            continue

        perimeter_cube.remove(curr_cube)

        # moves can be in 6 directions (up, down, forward, back, left, right)
        for ds in sides:
            next_cube = tuple(curr_cube[i] + ds[i] for i in range(3))
            if next_cube not in coords and next_cube in perimeter_cube:
                q.append(next_cube)

    # BFS finished, we should now have only trapped air in the
    # perimeter_cube set

    # calculate sides of the trapped cubes that are adjacent to sides of the
    # actual cubes
    # Generate cubes instances out of the trapped ones
    trapped = [Cube(*c) for c in perimeter_cube]
    for cube in trapped:
        for s in sides:
            adj_cube = cube.adjacent(s)
            if adj_cube in coords:
                cube.sides -= 1
                assert cube.sides >= 0

    # since we eliminated all overlapping sides from the trapped air cubes,
    # the remaining sides that need to be discounted are the difference to
    # the total number of sides of the trapped air cubes (6 sides per air cube)
    trapped_sides = 6 * len(trapped) - sum(cube.sides for cube in trapped)

    return total_sides - trapped_sides


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
# Part 2: Start: 18:01 End: 19:10 (with dinner break until 18:50)

# Elapsed time to run part1: 0.00424 seconds.
# Part 1: 4548
# Elapsed time to run part2: 0.03911 seconds.
# Part 2: 2588
