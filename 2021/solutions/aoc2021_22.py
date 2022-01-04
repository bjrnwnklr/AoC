# Load any required modules. Most commonly used:

from io import open_code
import re
# from collections import defaultdict
from utils.aoctools import aoc_timer
import numpy as np
from itertools import product
from dataclasses import dataclass


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    regex = re.compile(r'(-?\d+)')
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            instr = line.strip().split()[0]
            dims = list(map(int, regex.findall(line.strip())))
            puzzle_input.append([instr, dims])

    return puzzle_input


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    init_proc_dim = 50

    grid = np.zeros((init_proc_dim * 2 + 1, init_proc_dim *
                    2 + 1, init_proc_dim * 2 + 1), dtype=bool)

    for instr, dims in puzzle_input:
        # only look at cubes within the initiatilization dimensions
        if all(abs(x) <= init_proc_dim for x in dims):
            dims = [d + init_proc_dim for d in dims]
            min_x, max_x, min_y, max_y, min_z, max_z = dims
            state = True if instr == 'on' else False
            grid[min_x:max_x+1, min_y:max_y+1, min_z:max_z+1] = state

    result = grid.sum()

    return result


@dataclass
class Cube:
    instr: str
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    def volume(self: 'Cube') -> int:
        """Returns the cubic volume of the cube."""
        return (
            (abs(self.max_x - self.min_x) + 1) *
            (abs(self.max_y - self.min_y) + 1) *
            (abs(self.max_z - self.min_z) + 1)
        )


def overlap(a: Cube, b: Cube) -> bool:
    """Determine if two cubes overlap."""
    return (
        (a.max_x >= b.min_x and b.max_x >= a.min_x) and
        (a.max_y >= b.min_y and b.max_y >= a.min_y) and
        (a.max_z >= b.min_z and b.max_z >= a.min_z)
    )


def intersection(bg: Cube, fg: Cube) -> Cube:
    """Return the Cube resulting from the intersection of two overlapping cubes.

    To calculate the On/Off state, the cubes need to be in order of appearance - background and foreground.
    The foreground state determines the resulting state of the cube.
    """
    assert overlap(bg, fg) == True

    # sort values on each axis and take the two middle ones to determine the overlap
    min_x, max_x = sorted([bg.min_x, bg.max_x, fg.min_x, fg.max_x])[1:3]
    min_y, max_y = sorted([bg.min_y, bg.max_y, fg.min_y, fg.max_y])[1:3]
    min_z, max_z = sorted([bg.min_z, bg.max_z, fg.min_z, fg.max_z])[1:3]

    # the On/Off state is determined by the following logic:
    # - combining two On cubes: overlap gets Off state as we don't want to double count the overlap twice
    # - combining On (bg) and Off (fg) cube: intersection is Off as we need to subtract it
    # - combining Off (bg) and On (fg) cube: intersection is On as we need to add it back
    # - combining Off (bg) and Off (bg) cube: intersection is On as we don' double count the overlap twice
    match bg.instr:
        case 'on':
            instr = 'off'
        case 'off':
            instr = 'on'

    return Cube(instr, min_x, max_x, min_y, max_y, min_z, max_z)


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # find the min / max for each dimension of ON instructions
    cubes = [Cube(x, *y) for x, y in puzzle_input]
    resulting_cubes = []

    for fg in cubes:
        # print(f'Processing cube {fg}.')
        new_cubes = [
            intersection(bg, fg)
            for bg in resulting_cubes
            if overlap(bg, fg)
        ]
        if new_cubes:
            resulting_cubes.extend(new_cubes)

        # print(f'Found {len(new_cubes)} overlaps: {new_cubes}')

        # Do not add Off cubes to the resulting cubes as only their intersections with other cubes are relevant.
        if fg.instr == 'on':
            resulting_cubes.append(fg)

    # print(f'Resulting cubes: {len(resulting_cubes)}. {resulting_cubes}')
    on_cubes = sum(
        x.volume() if x.instr == 'on' else -x.volume() for x in resulting_cubes
    )
    return on_cubes


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/22.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 17:42 End: 18:04 (off by one error on dimension of grid)
# Part 2: Start: 18:05 End: 18:05 (next day)

# Elapsed time to run part1: 0.00159 seconds.
# Part 1: 607657
# Elapsed time to run part2: 1.09830 seconds.
# Part 2: 1187742789778677
