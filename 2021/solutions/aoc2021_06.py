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
    """Solve part 2 using recursion / memoization."""
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


@aoc_timer
def part3(puzzle_input):
    """Solve part 2 using a dictionary and just count the number of fish spawned."""
    fish = defaultdict(int)

    for f in puzzle_input:
        fish[f] += 1

    t = 256
    for _ in range(t):
        new_fish = defaultdict(int)
        for f, cnt in fish.items():
            if f == 0:
                new_fish[6] += cnt
                new_fish[8] += cnt
            else:
                new_fish[f-1] += cnt

        fish = new_fish.copy()

    return sum(fish.values())


@aoc_timer
def part4(puzzle_input):
    """Solve part 2 using a list and just count the number of fish spawned."""
    fish = [0] * 9

    for f in range(7):
        fish[f] = puzzle_input.count(f)

    t = 256
    for _ in range(t):
        new_fish = [0] * 9
        for i in range(9):
            if i == 0:
                new_fish[6] += fish[0]
                new_fish[8] += fish[0]
            else:
                new_fish[i-1] += fish[i]

        fish = new_fish[:]

    return sum(fish)


@aoc_timer
def part5(puzzle_input):
    """Solve part 2 using a list and shifting the elements and just count the number of fish spawned."""
    fish = [0] * 9

    for f in range(7):
        fish[f] = puzzle_input.count(f)

    t = 256
    for _ in range(t):
        # shift left
        f = fish.pop(0)
        # add at pos 8
        fish.append(f)
        # increment #6
        fish[6] += f

    return sum(fish)


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

    # Solve part 2 and print the answer
    p3 = part3(puzzle_input)
    print(f'Part 3: {p3}')

    # Solve part 2 and print the answer
    p4 = part4(puzzle_input)
    print(f'Part 4: {p4}')

    # Solve part 2 and print the answer
    p5 = part5(puzzle_input)
    print(f'Part 5: {p5}')

# Part 1: Start: 17:47 End: 18:01
# Part 2: Start: 18:02 End: 18:18

"""
Elapsed time to run part1: 0.62157 seconds.
Part 1: 388419
Elapsed time to run part2: 0.34589 seconds.
Part 2: 1740449478328
Elapsed time to run part3: 0.00083 seconds.
Part 3: 1740449478328
Elapsed time to run part4: 0.00062 seconds.
Part 4: 1740449478328
Elapsed time to run part5: 0.00007 seconds.
Part 5: 1740449478328
"""
