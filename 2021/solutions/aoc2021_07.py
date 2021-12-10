# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
from utils.aoctools import aoc_timer
from functools import lru_cache


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = [
            int(n) for n in f.readline().strip().split(',')
        ]

    return puzzle_input


def calc_pos(puzzle_input, cost):
    min_crab = min(puzzle_input)
    max_crab = max(puzzle_input)

    crab_distribution = defaultdict(int)
    for c in puzzle_input:
        crab_distribution[c] += 1

    # now iterate through all positions between min and max
    min_fuel = 1_000_000_000
    min_p = 10_000_000
    for p in range(min_crab, max_crab + 1):
        fuel = sum(cost(abs(p - c)) * crab_distribution[c]
                   for c in crab_distribution)
        if fuel < min_fuel:
            min_fuel = fuel
            min_p = p

    print(f'Min Fuel: {min_fuel}')
    print(f'Position: {min_p}')

    return min_fuel


def cost_part1(dist):
    return dist


@lru_cache
def cost_part2(dist):
    return sum(range(dist + 1))


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    return calc_pos(puzzle_input, cost_part1)


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return calc_pos(puzzle_input, cost_part2)


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/07.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 18:52 End: 19:06
# Part 2: Start: 19:07 End: 19:17

"""
Min Fuel: 352331
Position: 349
Elapsed time to run part1: 0.18057 seconds.
Part 1: 352331
Min Fuel: 99266250
Position: 488
Elapsed time to run part2: 10.02159 seconds.
Part 2: 99266250
"""
