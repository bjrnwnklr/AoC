# Load any required modules. Most commonly used:

# import re
from collections import defaultdict

# from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        raw_rules, raw_printing = f.read().split("\n\n")
        rules = defaultdict(list)
        for line in raw_rules.strip().split("\n"):
            left, right = list(map(int, line.split("|")))
            rules[left].append(right)

        printing = []
        for line in raw_printing.strip().split("\n"):
            printing.append(list(map(int, line.split(","))))

    return rules, printing


# @aoc_timer
def part1(rules, printing):
    """Solve part 1. Return the required output value."""
    result = 0
    for pages in printing:
        correct_order = True
        for i, left in enumerate(pages):
            for next_page in pages[i + 1 :]:
                if next_page not in rules[left]:
                    correct_order = False
                    break
            if not correct_order:
                break
        # if we get here, either all pages have been processed
        # or we found a page that does not meet the rule and can stop
        if correct_order:
            result += pages[len(pages) // 2]

    return result


# @aoc_timer
def part2(rules, printing):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    rules, printing = load_input("input/05.txt")

    # Solve part 1 and print the answer
    p1 = part1(rules, printing)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(rules, printing)
    print(f"Part 2: {p2}")

# Part 1: Start: 16:21 End: 16:44
# Part 2: Start: 16:45 End:
