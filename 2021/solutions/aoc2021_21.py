# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer
from itertools import product
from collections import Counter
# from functools import reduce
# import operator
from functools import cache, lru_cache


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

    {6: 7, 5: 6, 7: 6, 4: 3, 8: 3, 3: 1, 9: 1}
    """
    return [
        sum(d) for d in product(range(1, 4), repeat=3)
    ]


# Global counter for dirac_dice
c = Counter(dirac_dice(3))


@cache
def score_round(p: int, roll: int) -> int:
    """Score one round of dice rolls for any one player."""
    return (p + roll - 1) % 10 + 1


@aoc_timer
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


@cache
def who_wins(p1: int, s1: int, p2: int, s2: int, universes: int) -> tuple[int]:
    """Recursive function that returns how many times player one vs player two wins
    given a starting position, starting score for each player 
    and the number of universes this represents.
    """

    # winning score counter
    w1 = w2 = 0

    # go through each next round of 3 dice (results can only be 3-9)
    for roll, freq in c.items():

        # use fresh values for each round
        new_p1 = p1
        new_s1 = s1

        # calculate new position and scores for the player whose turn it is
        new_p1 = score_round(new_p1, roll)
        new_s1 += new_p1
        # if player wins this round, stop and add up number of won universes
        if new_s1 >= 21:
            w1 += freq * universes
            continue

        # nobody won this round so go to next turn. Swap around who is next in arguments.
        new_w1, new_w2 = who_wins(
            p2, s2, new_p1, new_s1, universes * freq)
        # since we swapped the players, reverse the winning scores to add the correct cases
        w1 += new_w2
        w2 += new_w1

    return w1, w2


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    p1 = puzzle_input[0]
    p2 = puzzle_input[1]
    s1 = s2 = 0

    win1, win2 = who_wins(p1, s1, p2, s2, 1)

    return max(win1, win2)


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
# Part 2: Start: 18:34 End: 17:39 (next day, stuck with slow results)

# cycles=861, s1=1008, s2=641
# Elapsed time to run part1: 0.00019 seconds.
# Part 1: 551901
# Elapsed time to run part2: 1.54390 seconds.
# Part 2: 272847859601291
