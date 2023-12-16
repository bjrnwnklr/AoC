# Load any required modules. Most commonly used:

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


def solve_line(springs, broken_groups, result, memo):
    """Attempt to solve a line of springs recursively."""
    if (springs, tuple(broken_groups), result) in memo:
        return memo[(springs, tuple(broken_groups), result)]

    if springs == "" and len(broken_groups) > 0:
        # empty string but groups left to do, so no match
        inner_result = 0
    elif springs == "" and len(broken_groups) == 0:
        # empty string and no groups left do, must be a match
        inner_result = 1
    elif len(springs) > 0 and len(broken_groups) == 0:
        # no groups left, but string left
        if "#" in springs:
            # no groups left but # still in remaining string
            # means no match
            inner_result = 0
        else:
            inner_result = 1
    # if we get here, there is still string left and also groups
    elif springs[0] == ".":
        # remove as not useful, and process from next char
        inner_result = result + solve_line(springs[1:], broken_groups, result, memo)
    elif springs[0] == "?":
        inner_result = (
            result
            + solve_line("." + springs[1:], broken_groups, result, memo)
            + solve_line("#" + springs[1:], broken_groups, result, memo)
        )
    elif springs[0] == "#":
        # check if the first group fits in (must be ? or #)
        group = broken_groups[0]
        if len(springs) >= group and all(c != "." for c in springs[:group]):
            if len(springs[group:]) == 0 or springs[group] != "#":
                # we found an exact count of # - no directly following #
                # means we can continue searching after the group
                # skip the next character as it needs to be a .
                # a ? would result in double counts as it would be
                # valid for #
                inner_result = result + solve_line(
                    springs[group + 1 :], broken_groups[1:], result, memo
                )
            else:
                # # is directly following, but group is shorter. we can stop here
                inner_result = 0
        else:
            # string is either shorter than required length of group,
            # or there are . in the length of the group
            inner_result = 0
    else:
        # group is longer than the next # and ? combined
        # we can stop searching with this configuration
        inner_result = 0

    memo[(springs, tuple(broken_groups), result)] = inner_result
    return inner_result


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # parse the input
    memo = dict()
    result = 0
    for line in puzzle_input:
        springs, groups = line.split()
        broken_groups = list(map(int, groups.split(",")))
        line_result = solve_line(springs, broken_groups, 0, memo)
        result += line_result

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # parse the input
    memo = dict()
    result = 0
    for line in puzzle_input:
        springs, groups = line.split()
        broken_groups = list(map(int, groups.split(",")))
        # add additional springs and groups
        springs = "?".join(springs for _ in range(5))
        broken_groups = broken_groups * 5

        line_result = solve_line(springs, broken_groups, 0, memo)
        result += line_result

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/12.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 13:52 End: 16:35 (with break)
# Part 2: Start: 16:36 End: 18:36 (rewrote part 1 completely to use recursion)

# Elapsed time to run part1: 0.02569 seconds.
# Part 1: 7350
# Elapsed time to run part2: 0.76729 seconds.
# Part 2: 200097286528151
