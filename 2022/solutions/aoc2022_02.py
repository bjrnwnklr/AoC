# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


RPS = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}
RPS2 = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 3, "Z": 6}


def translate_rps(line, part=1):
    """Translates an input line 'A Y' into numbers
    (1, 2)"""
    l, r = line.split()
    if part == 1:
        d = RPS
    else:
        d = RPS2
    return (d[l], d[r])


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.
    A, X = Rock     0
    B, Y = Paper    1
    C, Z = Scissors 2

    Lose:
    A Z (Rock Scissors) 0 2 = -2 = 1 (-2 % 3 == 1)
    B X (Paper Rock) 1 0 = 1
    C Y (Scissors Paper) 2 1 = 1

    Draw:
    A X 0 0 = 0
    B Y 1 1 = 0
    C Z 2 2 = 0

    Win:
    C X (Scissors Rock) 2 0 = 2
    A Y (Rock Paper)    0 1 = -1 = 2 (-1 % 3 == 1)
    B Z (Paper Scissors) 1 2 = -1 = 2
    """
    score = 0
    for line in puzzle_input:
        l, r = translate_rps(line)
        # score always includes value of my selected shape
        score += r + 1
        result = (l - r) % 3
        match result:
            case 0:
                # draw
                score += 3
            case 1:
                # elf wins
                pass
            case 2:
                # you win
                score += 6

    return score


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    X lose 0
    Y draw 3
    Z win  6
    """
    score = 0
    for line in puzzle_input:
        l, r = translate_rps(line, 2)
        # add win / draw / loss to score
        score += r
        result = 0
        match r:
            case 0:
                # loss, add 2 to l, adjust so we get
                # 3 instead of 0
                result = (l - 1) % 3
            case 3:
                # draw, just add left value
                result = l
            case 6:
                # win, add 1 to l
                result = (l + 1) % 3

        score += result + 1

    return score


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/02.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 17:38 End: 18:02
# Part 2: Start: 18:03 End: 18:50
