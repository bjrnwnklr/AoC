# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer


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

# Part 1: Start: 17:39 End:
# Part 2: Start:  End:
