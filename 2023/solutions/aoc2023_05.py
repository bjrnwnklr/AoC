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
        return f.read()


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # split input into sections
    sections = puzzle_input.split("\n\n")

    # get list of seeds
    seeds = list(map(int, sections[0].split(":")[1].split()))

    # process each section
    for section in sections[1:]:
        # first line is the recipe - might not actually be required?
        lines = section.strip().split("\n")
        source, _, destination = lines[0].split()[0].split("-")
        # read mapping table into a list
        mapping = []
        for line in lines[1:]:
            mapping.append(list(map(int, line.strip().split())))

        # generate mapped seed value
        for i, seed in enumerate(seeds):
            for d, s, r in mapping:
                if seed in range(s, s + r):
                    # found the seed in the range and translated
                    # according to mapping by updating the seeds table
                    # skip rest of mappings
                    seeds[i] = d + seed - s
                    continue

    # processed all seeds through all mapping recipes
    # find minimum seed value

    return min(seeds)


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # split input into sections
    sections = puzzle_input.split("\n\n")

    # get list of seeds
    raw_seeds = list(map(int, sections[0].split(":")[1].split()))
    seeds = []
    # generate a list of the seed intervals with start, end (inclusive)
    for i in range(0, len(raw_seeds), 2):
        seeds.append((raw_seeds[i], raw_seeds[i] + raw_seeds[i + 1] - 1))

    # process each section
    for section in sections[1:]:
        # first line is the recipe - might not actually be required?
        lines = section.strip().split("\n")
        # read mapping table into a list
        mapping = []
        for line in lines[1:]:
            mapping.append(list(map(int, line.strip().split())))

        # generate new mapping: start, end, translation (e.g. +2)
        translation = {}
        for d, s, r in mapping:
            translation[(s, s + r - 1)] = d - s

        # process each seed range and see if it fits into a Translation
        # - translate it to new seed range if yes
        # - split it into two or more ranges if no and translate these
        new_seeds = []
        sorted_translations = sorted(translation.keys())
        while seeds:
            start, end = seeds.pop(0)
            # determine translation range where start is
            for r in sorted_translations:
                # check where start and end date fall
                if start < r[0] and end < r[0]:
                    # if both start and end lower than lowest interval
                    # translate with +0 and go to next interval
                    new_seeds.append((start, end))
                    break
                if start < r[0] and end >= r[0]:
                    # start is outside, end is somewhere higher
                    # add untranslated interval
                    new_seeds.append((start, r[0] - 1))
                    # and create new seed interval to keep checking
                    seeds.append((r[0], end))
                    break
                if r[0] <= start <= r[1] and end <= r[1]:
                    # seed interval is completely in the translation interval
                    new_seeds.append((start + translation[r], end + translation[r]))
                    break
                if r[0] <= start <= r[1] and end > r[1]:
                    # start is in interval but end is higher
                    # translate part that is in interval
                    new_seeds.append((start + translation[r], r[1] + translation[r]))
                    # create new seed interval for the rest
                    seeds.append((r[1] + 1, end))
                    break
            else:
                # for loop didnt find a range that had the start or end seed
                # meaning start and end are higher than any translation range
                # add untranslated range to new ranges
                new_seeds.append((start, end))

        # done with this section, set new seeds
        seeds = new_seeds[:]

    # processed all seeds through all mapping recipes
    # find minimum seed value
    result = min(s for s, e in seeds)

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/05.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 11:19 End: 11:56
# Part 2: Start: 11:57 End: 14:53 (incl break)

# Elapsed time to run part1: 0.00088 seconds.
# Part 1: 218513636
# Elapsed time to run part2: 0.00134 seconds.
# Part 2: 81956384
