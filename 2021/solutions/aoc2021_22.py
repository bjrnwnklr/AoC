# Load any required modules. Most commonly used:

from io import open_code
import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer
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


# @aoc_timer
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


def overlap(a: Cube, b: Cube) -> bool:
    """Determine if two cubes overlap."""
    return (
        (a.max_x >= b.min_x and b.max_x >= a.min_x) and
        (a.max_y >= b.min_y and b.max_y >= a.min_y) and
        (a.max_z >= b.min_z and b.max_z >= a.min_z)
    )


def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # find the min / max for each dimension of ON instructions
    cubes = [Cube(x, *y) for x, y in puzzle_input]
    on_cubes = []

    while cubes:
        a = cubes.pop(0)
        if a.instr == 'on':
            on_cubes.append(a)
        else:
            for b in on_cubes:
                if overlap(a, b):
                    print(f'Overlapping: {a=}, {b=}')

    return 1


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
# Part 2: Start: 18:05 End:

""" 
Naive approach to create an empty array spanning the full cube:

def part2(puzzle_input):
    find dimensions of grid
    dim_min_x = 0
    dim_max_x = 0
    dim_min_y = 0
    dim_max_y = 0
    dim_min_z = 0
    dim_max_z = 0
    for _, dims in puzzle_input:
        c_min_x, c_max_x, c_min_y, c_max_y, c_min_z, c_max_z = dims
        if c_min_x < dim_min_x:
            dim_min_x = c_min_x
        if c_min_y < dim_min_y:
            dim_min_y = c_min_y
        if c_min_z < dim_min_z:
            dim_min_z = c_min_z
        if c_max_x > dim_max_x:
            dim_max_x = c_max_x
        if c_max_y > dim_max_y:
            dim_max_y = c_max_y
        if c_max_z > dim_max_z:
            dim_max_z = c_max_z
    x_dim = dim_max_x - dim_min_x + 1
    y_dim = dim_max_y - dim_min_y + 1
    z_dim = dim_max_z - dim_min_z + 1

    grid = np.zeros((x_dim, y_dim, z_dim), dtype=bool)

    for instr, dims in puzzle_input:
        min_x, max_x, min_y, max_y, min_z, max_z = dims
        state = True if instr == 'on' else False
        grid[min_x + abs(dim_min_x):max_x + abs(dim_min_x) + 1, min_y + abs(dim_min_y):max_y +
             abs(min_dim_y) + 1, min_z + abs(dim_min_z):max_z + abs(dim_min_z) + 1] = state

    result = grid.sum()

Resulted in glorious failure!

>       grid = np.zeros((x_dim, y_dim, z_dim), dtype=bool)
E       numpy.core._exceptions._ArrayMemoryError: Unable to allocate 12.5 PiB for an array with shape (240976, 243419, 240817) and data type bool

solutions/aoc2021_22.py:75: MemoryError


Next approach with set arithmetic:

def part2(puzzle_input):

    grid = set()

    for instr, dims in puzzle_input:
        min_x, max_x, min_y, max_y, min_z, max_z = dims
        state = True if instr == 'on' else False

        new_slice = {
            (x, y, z)
            for x, y, z in product(range(min_x, max_x + 1), range(min_y, max_y + 1), range(min_z, max_z + 1))
        }
        if state:
            # ON, so we add to the switched on cubes
            grid |= new_slice
        else:
            # OFF, so we remove from the switched cubes
            grid -= new_slice

    return len(grid)

got killed by a out-of-memory error!

[25375.451167] [   3352]  1000  3352  5796921  3855985 37031936   721456             0 python
[25375.451168] oom-kill:constraint=CONSTRAINT_NONE,nodemask=(null),cpuset=/,mems_allowed=0,global_oom,task_memcg=/,task=python,pid=3352,uid=1000
[25375.451210] Out of memory: Killed process 3352 (python) total-vm:23187684kB, anon-rss:15423936kB, file-rss:4kB, shmem-rss:0kB, UID:1000 pgtables:36164kB oom_score_adj:0
[25375.781681] oom_reaper: reaped process 3352 (python), now anon-rss:0kB, file-rss:0kB, shmem-rss:0kB
"""
