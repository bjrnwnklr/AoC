# Load any required modules. Most commonly used:

# import re
from collections import defaultdict

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

    return puzzle_input


TYPES = {
    "five_of_a_kind": 6,
    "four_of_a_kind": 5,
    "full_house": 4,
    "three_of_a_kind": 3,
    "two_pair": 2,
    "one_pair": 1,
    "high_card": 0,
}

CARDS = {k: i for i, k in enumerate(list("23456789TJQKA"))}
CARDS_2 = {k: i for i, k in enumerate(list("J23456789TQKA"))}


def hand_type(hand):
    """Return the type of hand the provided hand is."""
    d = defaultdict(int)
    for c in list(hand):
        d[c] += 1

    if max(d.values()) == 5:
        return TYPES["five_of_a_kind"]
    elif max(d.values()) == 4:
        return TYPES["four_of_a_kind"]
    elif max(d.values()) == 3:
        # check if we have 3 and 2 in the counts
        if 2 in d.values():
            return TYPES["full_house"]
        else:
            return TYPES["three_of_a_kind"]
    elif max(d.values()) == 2:
        pairs = sum(1 for x in d.values() if x == 2)
        if pairs == 2:
            return TYPES["two_pair"]
        else:
            assert pairs == 1
            return TYPES["one_pair"]
    else:
        return TYPES["high_card"]


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    hands = []
    for line in puzzle_input:
        hand, bid = line.split()
        bid = int(bid.strip())
        hands.append((hand, hand_type(hand), bid))

    # now run second compare to calculate score
    sorted_hands = sorted(
        hands, key=lambda x: (x[1], tuple(CARDS[y] for y in list(x[0]))), reverse=True
    )
    # reverse the sorted hands
    sorted_hands = sorted_hands[::-1]
    result = sum(h[2] * i for i, h in enumerate(sorted_hands, start=1))

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    hands = []
    for line in puzzle_input:
        hand, bid = line.split()
        bid = int(bid.strip())
        # add all possible hands with a joker - replace
        # any J with any type of card and see what the highest
        # output is
        # also need to take care to pick the strongest card i.e.
        # if there are multiple options for a four-of-a-kind,
        # it doesnt matter which one we pick as the tie-breaker
        # is the order of the CARDS
        highest_type = 0
        for j in list("23456789TQKA"):
            joker_hand = hand.replace("J", j)
            highest_type = max(highest_type, hand_type(joker_hand))

        hands.append((hand, highest_type, bid))

    # now run second compare to calculate score
    sorted_hands = sorted(
        hands, key=lambda x: (x[1], tuple(CARDS_2[y] for y in list(x[0]))), reverse=True
    )
    # reverse the sorted hands
    sorted_hands = sorted_hands[::-1]
    result = sum(h[2] * i for i, h in enumerate(sorted_hands, start=1))

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/07.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 15:31 End: 16:09
# Part 2: Start: 16:10 End: 16:21

# Elapsed time to run part1: 0.00312 seconds.
# Part 1: 249483956
# Elapsed time to run part2: 0.02470 seconds.
# Part 2: 252137472
