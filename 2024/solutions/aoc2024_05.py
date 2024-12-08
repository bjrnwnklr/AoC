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
        raw_rules, raw_printing = f.read().split("\n\n")
        rules = defaultdict(list)
        for line in raw_rules.strip().split("\n"):
            left, right = list(map(int, line.split("|")))
            rules[left].append(right)

        printing = []
        for line in raw_printing.strip().split("\n"):
            printing.append(list(map(int, line.split(","))))

    return rules, printing


@aoc_timer
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


def sort_instructions(rules):
    # sort the rules by their length - the shortest rule
    # will be processed first
    sorted_rules = sorted(rules, key=lambda x: len(rules[x]), reverse=True)
    # add the page number from the rule with just one element
    # as there should be no rule for that one
    # in the example, this is 29: [13] - 13 has no rule
    for n in rules[sorted_rules[-1]]:
        if n not in sorted_rules:
            sorted_rules.append(n)
    return sorted_rules


def get_new_rules(rules, pages):
    """Generate a reduced set of rules from the overall rules,
    only including the numbers that are in the pages to be processed.


    """
    copy_rules = {
        k: [n for n in v if n in pages] for k, v in rules.items() if k in pages
    }
    return copy_rules


@aoc_timer
def part2(rules, printing):
    """Solve part 2. Return the required output value.
    Each rule has 46 members, and there are 46 rules. Each number appears in
    at least one rule.

    However, when processing the individual page sets, the rules become much
    simpler for just this set of pages.

    This produces a much reduced set of rules, where each rule has one
    member less than the previous rule, which can then be used to sort
    the rules and start processing from the one that has no members
    - this will be the last number.

    Example:
    Processing pages: [13, 14, 76, 77, 74, 64, 29, 27, 26, 41, 15]
    13: [77, 27, 15, 14, 74, 26, 76, 64, 41, 29]
    14: [77, 29, 15, 76, 74, 27, 64, 41, 26]
    76: [27, 77, 29, 64, 74, 41, 15, 26]
    77: [26, 29, 74, 41, 27, 64, 15]
    74: [29, 26, 27, 15, 64, 41]
    64: [15, 41, 27, 29, 26]
    29: [26, 15, 41, 27]
    27: [41, 15, 26]
    26: [41, 15]
    41: [15]
    15: []
    Sorted rules: [13, 14, 76, 77, 74, 64, 29, 27, 26, 41, 15]
    """
    result = 0
    for pages in printing:
        # create the reduced set of rules
        copy_rules = get_new_rules(rules, pages)
        # sort the resulting page numbers by length of their ruleset
        sorted_pages = sort_instructions(copy_rules)
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
        if not correct_order:
            # trigger correct order sorting here
            new_page_order = [x for x in sorted_pages if x in pages]
            # print(f"Found an incorrectly ordered page list: {pages}")
            # print(f"Reordering: {new_page_order}")
            result += new_page_order[len(new_page_order) // 2]
            # print(f"Updated result: {result}")

    return result


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
# Part 2: Start: 16:45 End: 17:30

# Elapsed time to run part1: 0.00186 seconds.
# Part 1: 5713
# Elapsed time to run part2: 0.01445 seconds.
# Part 2: 5180
