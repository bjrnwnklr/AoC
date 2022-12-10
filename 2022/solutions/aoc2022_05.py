# Load any required modules. Most commonly used:

import re

from collections import deque

from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        # split input into two parts
        # - stacks
        # - instructions
        s, i = f.read().split("\n\n")

        rows = []
        # parse the stacks
        for line in s.split("\n"):
            # each segment is 4 characters: [L]_
            num_stacks = (len(line) // 4) + 1
            # find each crate at (stack * 4) + 1 (2nd position)
            rows.append([line[(stack * 4) + 1] for stack in range(num_stacks)])

        # create stacks by going through the crates and adding
        # them to each stack
        # determine number of stacks and set up stacks
        stacks = [deque([]) for _ in range(len(rows[-1]))]

        # fill stacks - left = top, right = bottom
        for row in rows[:-1]:
            for col, crate in enumerate(row):
                if crate != " ":
                    stacks[col].append(crate)

        # find all numbers in the instructions
        regex = re.compile(r"(\d+)")

        instructions = []
        for line in i.split("\n"):
            matches = regex.findall(line.strip())
            if matches:
                instructions.append(list(map(int, matches)))

    return (stacks, instructions)


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    stacks, instructions = puzzle_input

    # move crates
    for count, s_from, s_to in instructions:
        for _ in range(count):
            # pop element from s_from
            crate = stacks[s_from - 1].popleft()
            # push element into s_to
            stacks[s_to - 1].appendleft(crate)

    # get top crates
    result = "".join([s[0] for s in stacks])

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    stacks, instructions = puzzle_input

    # move crates
    for count, s_from, s_to in instructions:
        temp_stack = deque([])
        for _ in range(count):
            # pop element from s_from
            crate = stacks[s_from - 1].popleft()
            # push crate into temp_stack
            temp_stack.append(crate)
        # reverse the temp stack and then extendleft to the
        # stack (extendleft does individual appends, so needs
        # to be first reversed)
        temp_stack.reverse()
        stacks[s_to - 1].extendleft(temp_stack)

    # get top crates
    result = "".join([s[0] for s in stacks])
    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/05.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    puzzle_input = load_input("input/05.txt")
    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 15:08 End: 15:55
# Part 2: Start: 15:56 End: 16:14

# Elapsed time to run part1: 0.00060 seconds.
# Part 1: RNZLFZSJH
# Elapsed time to run part2: 0.00075 seconds.
# Part 2: CNSFCGJSM
