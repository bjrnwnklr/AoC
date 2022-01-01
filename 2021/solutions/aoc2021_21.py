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
def who_wins(p1: int, s1: int, p2: int, s2: int, turn: int, universes: int) -> tuple[int]:
    """Recursive function that returns how many times player one vs player two wins
    given a starting position, starting score for each player 
    and the number of universes this represents.
    """
    # if no winner, go through next iteration of scores by running each combination
    # print(
    #     f"Player {turn + 1}'s turn: {p1=}, {s1=}, {p2=}, {s2=}, {turn=}, {universes=}.")

    w1 = w2 = 0
    for roll in c:

        cases = c[roll]
        new_p1 = p1
        new_p2 = p2
        new_s1 = s1
        new_s2 = s2

        # calculate new position and scores for the player whose turn it is
        # player1 = 0
        # player2 = 1
        if turn == 0:
            new_p1 = score_round(new_p1, roll)
            new_s1 += new_p1
            if new_s1 >= 21:
                w1 += cases * universes
                # print(
                #     f'Player 1 won with {new_s1=}, adding {cases * universes} wins. {w1=}')
                continue
        else:
            new_p2 = score_round(new_p2, roll)
            new_s2 += new_p2
            if new_s2 >= 21:
                w2 += cases * universes
                # print(
                #     f'Player 2 won with {new_s2=}, adding {cases * universes} wins. {w2=}')
                continue

        new_w1, new_w2 = who_wins(
            new_p1, new_s1, new_p2, new_s2, (turn + 1) % 2, universes * cases)
        w1 += new_w1
        w2 += new_w2

    # print(f'Returning {w1=}, {w2=}')
    return w1, w2


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    p1 = puzzle_input[0]
    p2 = puzzle_input[1]
    s1 = s2 = 0
    win1 = win2 = 0

    win1, win2 = who_wins(p1, s1, p2, s2, 0, 1)

    return max(win1, win2)


@aoc_timer
def part2_incorrect(puzzle_input):
    """Solve part 2. Return the required output value."""

    # TODO:
    # 12_676_622_843_967_107_256 (from incorrect attempt)
    #         18_043_431_879_060
    #        444_356_092_776_315 (from part 2 test case)

    d = dirac_dice(3)
    c = Counter(d)
    print(c)

    p1 = puzzle_input[0]
    p2 = puzzle_input[1]
    s1 = s2 = 0
    win1 = win2 = 0
    winning_score = 21

    # player 1 pos, player 1 score, player 2 pos, player 2 score, next pair of dice rolls (r1, r2)
    # list of dice rolls for p1 / p2 so far), universes covered
    q = [(p1, s1, p2, s2, [], [], 1)]

    while q:

        p1, s1, p2, s2, cur_roll, cur_path, universes = q.pop()
        # print(f'({p1=}, {s1=}, {p2=}, {s2=}, {cur_roll=}, {cur_path=}, {universes=})')
        if cur_roll:
            cur_path.extend(cur_roll)
            universes *= c[cur_roll[0]] * c[cur_roll[1]]

            p1 = score_round(p1, cur_roll[0])
            s1 += p1
            # check if any player won
            if s1 >= winning_score:
                # player 1 won
                win1 += universes
                # print(f'Player 1 won. {win1=}')
                continue

            p2 = score_round(p2, cur_roll[1])
            s2 += p2
            if s2 >= winning_score:
                # player 2 won
                win2 += universes
                # print(f'Player 2 won. {win2=}')
                continue

        for roll in product(c, repeat=2):
            q.append((p1, s1, p2, s2, roll, cur_path[:], universes))

    print(f'Player 1 winning: {win1}, player 2 winning: {win2}')

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

# cycles=861, s1=1008, s2=641
# Elapsed time to run part1: 0.00019 seconds.
# Part 1: 551901
# Elapsed time to run part2: 1.79995 seconds.
# Part 2: 272847859601291
