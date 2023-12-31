# Load any required modules. Most commonly used:

import re

from collections import defaultdict
from copy import deepcopy
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines

    # unsigned ints
    regex = re.compile(r"(\d+)")

    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            matches = regex.findall(line.strip())
            if matches:
                puzzle_input.append(list(map(int, matches)))

    return puzzle_input


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    bricks = puzzle_input
    # sort bricks by first z ascending - from bottom to top
    bricks = sorted(bricks, key=lambda x: x[2])
    # tower is a dictionary of (x, y, z) coordinates and the id of the brick
    # occupying the coordinate; 0 if no brick is there
    tower = defaultdict(int)
    # store list bricks dependent on each other
    # brick: set of bricks it depends on
    depends_on = defaultdict(set)
    supported_by = defaultdict(set)
    # go through each brick and settle it
    for ind, brick in enumerate(bricks, start=1):
        # get the coordinates occupied by the brick - they only stretch in one dimension
        brick_coordinates = [
            (x, y, z)
            for x in range(brick[0], brick[3] + 1)
            for y in range(brick[1], brick[4] + 1)
            for z in range(0, brick[5] - brick[2] + 1)
        ]
        # go down through z axis, starting from current z position of brick
        # to 1 (lowest position)
        # if all of the x and y coordinates are free, drop the brick there
        for z in range(brick[2], 0, -1):
            if all(tower[(x, y, z)] == 0 for x, y, _ in brick_coordinates):
                lowest = z
            else:
                break
        # drop brick at lowest z position
        for x, y, z in brick_coordinates:
            tower[(x, y, z + lowest)] = ind
            # check bricks that are supporting this brick:
            # bricks that are below the current position
            if (
                tower[(x, y, z + lowest - 1)] != 0
                and tower[(x, y, z + lowest - 1)] != ind
            ):
                depends_on[ind].add(tower[(x, y, z + lowest - 1)])
                supported_by[tower[(x, y, z + lowest - 1)]].add(ind)

    # determine bricks that can be disintegrated by checking which ones
    # have a single dependency on this brick - these cannot be disintegrated
    result = 0
    for b in range(1, len(bricks) + 1):
        disintegration = True
        for supported in supported_by[b]:
            if len(depends_on[supported]) == 1:
                disintegration = False
                break
        if disintegration:
            result += 1

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    bricks = puzzle_input
    # sort bricks by first z ascending - from bottom to top
    bricks = sorted(bricks, key=lambda x: x[2])
    # tower is a dictionary of (x, y, z) coordinates and the id of the brick
    # occupying the coordinate; 0 if no brick is there
    tower = defaultdict(int)
    # store list bricks dependent on each other
    # brick: set of bricks it depends on
    depends_on = defaultdict(set)
    supported_by = defaultdict(set)
    # go through each brick and settle it
    for ind, brick in enumerate(bricks, start=1):
        # get the coordinates occupied by the brick - they only stretch in one dimension
        brick_coordinates = [
            (x, y, z)
            for x in range(brick[0], brick[3] + 1)
            for y in range(brick[1], brick[4] + 1)
            for z in range(0, brick[5] - brick[2] + 1)
        ]
        # go down through z axis, starting from current z position of brick
        # to 1 (lowest position)
        # if all of the x and y coordinates are free, drop the brick there
        for z in range(brick[2], 0, -1):
            if all(tower[(x, y, z)] == 0 for x, y, _ in brick_coordinates):
                lowest = z
            else:
                break
        # drop brick at lowest z position
        for x, y, z in brick_coordinates:
            tower[(x, y, z + lowest)] = ind
            # check bricks that are supporting this brick:
            # bricks that are below the current position
            if (
                tower[(x, y, z + lowest - 1)] != 0
                and tower[(x, y, z + lowest - 1)] != ind
            ):
                depends_on[ind].add(tower[(x, y, z + lowest - 1)])
                supported_by[tower[(x, y, z + lowest - 1)]].add(ind)

    # determine bricks that can be disintegrated by checking which ones
    # have a single dependency on this brick - these cannot be disintegrated
    result = 0
    for b in range(1, len(bricks) + 1):
        dp = deepcopy(depends_on)
        falling = 0
        q = [b]
        while q:
            to_remove = q.pop(0)
            for remove_from in supported_by[to_remove]:
                dp[remove_from].remove(to_remove)
                if len(dp[remove_from]) == 0:
                    # brick is not supported anymore, falls down
                    falling += 1
                    q.append(remove_from)
        result += falling

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/22.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 14:35 End: 15:51
# Part 2: Start: 15:52 End:

# Elapsed time to run part1: 0.06489 seconds.
# Part 1: 418
# Elapsed time to run part2: 5.54405 seconds.
# Part 2: 70702
