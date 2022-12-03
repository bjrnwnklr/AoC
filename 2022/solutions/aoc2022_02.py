# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer


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


RPS = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}


def translate_rps(line):
    """Translates an input line 'A Y' into numbers
    (1, 2)"""
    l, r = line.split()
    return (RPS[l], RPS[r])


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.
    A, X = Rock     1
    B, Y = Paper    2
    C, Z = Scissors 3

    Lose:
    A Z (Rock Scissors) 1 3 = -2 = 1 (-2 % 3 == 1)
    B X (Paper Rock) 2 1 = 1
    C Y (Scissors Paper) 3 2 = 1

    Draw:
    A X 1 1 = 0
    B Y 2 2 = 0
    C Z 3 3 = 0

    Win:
    C X (Scissors Rock) 3 1 = 2
    A Y (Rock Paper)    1 2 = -1 = 2 (-1 % 3 == 1)
    B Z (Paper Scissors) 2 3 = -1 = 2
    """
    score = 0
    for line in puzzle_input:
        l, r = translate_rps(line)
        # score always includes value of my selected shape
        score += r
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


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


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
# Part 2: Start: 18:03 End:
