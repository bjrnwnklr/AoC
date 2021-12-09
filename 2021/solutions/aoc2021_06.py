# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer
from functools import lru_cache


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for n in f.readline().strip().split(','):
            puzzle_input.append(int(n))

    return puzzle_input


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    cycles = 80
    t = 0
    fish = puzzle_input[:]

    while t < cycles:
        new_fish = []
        old_fish = []

        for f in fish:
            if f > 0:
                old_fish.append(f-1)
            elif f == 0:
                old_fish.append(6)
                new_fish.append(8)

        t += 1
        fish = old_fish[:] + new_fish[:]

    return len(fish)


@lru_cache()
def spawn_fish(n, t):
    if t == 0:
        return 1
    else:
        if n == 0:
            return spawn_fish(6, t-1) + spawn_fish(8, t-1)
        else:
            return spawn_fish(n-1, t-1)


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    t = 256
    result = sum(spawn_fish(f, t) for f in puzzle_input)

    return result


if __name__ == '__main__':
    # read the puzzle input
    # puzzle_input = load_input('testinput/06_1_1.txt')
    puzzle_input = load_input('input/06.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 17:47 End: 18:01
# Part 2: Start: 18:02 End: 18:18
