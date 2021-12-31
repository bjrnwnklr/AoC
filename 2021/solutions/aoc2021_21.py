# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer
from itertools import product


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(int((line.strip().split(':'))[1]))

    return puzzle_input


def deterministic_dice(n: int = 100) -> list[int]:
    """Generator: deterministic dice. Delivers sum of (1+2+3, 4+5+6, ...), 
    wrapping around at n (default 100)
    """
    i = 0
    while True:
        s = 0
        for _ in range(3):
            i = (i % n) + 1
            s += i
        yield s


def dirac_dice(n: int = 3):
    """Simulates all outcomes of a dirac dice.

    27 different combinations of 1, 2, 3 - 27 different universes for each 3 roll of dice.

    (1, 1, 1) 3
    (1, 1, 2) 4
    (1, 1, 3) 5
    (1, 2, 1) 4
    (1, 2, 2) 5
    (1, 2, 3) 6
    (1, 3, 1) 5
    (1, 3, 2) 6
    (1, 3, 3) 7
    (2, 1, 1) 4
    (2, 1, 2) 5
    (2, 1, 3) 6
    (2, 2, 1) 5
    (2, 2, 2) 6
    (2, 2, 3) 7
    (2, 3, 1) 6
    (2, 3, 2) 7
    (2, 3, 3) 8
    (3, 1, 1) 5
    (3, 1, 2) 6
    (3, 1, 3) 7
    (3, 2, 1) 6
    (3, 2, 2) 7
    (3, 2, 3) 8
    (3, 3, 1) 7
    (3, 3, 2) 8
    (3, 3, 3) 9
    """
    return [
        sum(d) for d in product(range(1, 4), repeat=3)
    ]


# @aoc_timer


def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    print()

    p1 = puzzle_input[0]
    p2 = puzzle_input[1]
    s1 = s2 = 0
    d = deterministic_dice(100)
    cycles = 0
    while s1 < 1000 and s2 < 1000:
        n = next(d)
        p1 = (p1 + n - 1) % 10 + 1
        s1 += p1
        # print(f'{n=} - {p1= }: {s1=}')
        cycles += 3
        if s1 >= 1000:
            break
        n = next(d)
        p2 = (p2 + n - 1) % 10 + 1
        s2 += p2
        # print(f'{n=} - {p2=}: {s2=}')
        cycles += 3

    print(f'{cycles=}, {s1=}, {s2=}')
    return min(s1, s2) * cycles


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    # TODO:
    #
    # Determine sum of player given:
    # - starting pos
    # - sum of dice rolls
    #
    # Since the results of the dirac dice are always 3, 4, 5, 6, 7, 8 or 9,
    # we should be able to cache some of the results to cover similar cases.
    # i.e. if current p1 result is x, the outcome for all cases resulting in 3
    # as the next roll should be the same for this round
    #
    print()

    p1 = puzzle_input[0]
    p2 = puzzle_input[1]
    s1 = s2 = 0
    d = deterministic_dice(3)
    cycles = 0
    while s1 < 21 and s2 < 21:
        n = next(d)
        p1 = (p1 + n - 1) % 10 + 1
        s1 += p1
        # print(f'{n=} - {p1= }: {s1=}')
        cycles += 3
        if s1 >= 1000:
            break
        n = next(d)
        p2 = (p2 + n - 1) % 10 + 1
        s2 += p2
        # print(f'{n=} - {p2=}: {s2=}')
        cycles += 3

    print(f'{cycles=}, {s1=}, {s2=}')
    return min(s1, s2) * cycles
    return 1


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/21.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 17:39 End: 18:33
# Part 2: Start: 18:34 End:
