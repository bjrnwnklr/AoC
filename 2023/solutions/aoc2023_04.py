# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    # Extract ints from the input
    #
    # signed ints
    # regex = re.compile(r"(-?\d+)")
    #
    # unsigned ints
    # regex = re.compile(r"(\d+)")
    #
    # with open(f_name, "r") as f:
    #     puzzle_input = []
    #     for line in f.readlines():
    #         matches = regex.findall(line.strip())
    #         if matches:
    #             puzzle_input.append(list(map(int, matches)))

    return puzzle_input


def parse_card(line):
    """Parse a card into two lists:
    - winning numbers
    - numbers you have
    """
    _, numbers = line.split(":")
    # ignore the card for now - might need later
    winning, held = numbers.split("|")
    win_num = list(map(int, winning.strip().split()))
    held_num = list(map(int, held.strip().split()))

    return win_num, held_num


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    result = 0
    for line in puzzle_input:
        winning, held = parse_card(line)
        p = 0
        for n in held:
            if n in winning:
                p += 1
        if p > 0:
            result += 2 ** (p - 1)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    card_count = len(puzzle_input)
    # dictionary that has how many of each card we have
    cards = {i: 1 for i in range(1, card_count + 1)}
    # iterate through cards
    for i, line in enumerate(puzzle_input, start=1):
        winning, held = parse_card(line)
        cards_won = 0
        for n in held:
            if n in winning:
                cards_won += 1
                cards[i + cards_won] += cards[i]

    result = sum(n for n in cards.values())

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/04.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 18:54 End: 19:04
# Part 2: Start: 19:05 End: 19:19

# Elapsed time to run part1: 0.00127 seconds.
# Part 1: 27454
# Elapsed time to run part2: 0.00137 seconds.
# Part 2: 6857330
