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
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def parse_grid(puzzle_input):
    """Parse the input into:
    - set of rocks
    - starting position
    - boundaries (width / height)"""
    rocks = set()
    width = len(puzzle_input[0])
    height = len(puzzle_input)
    for r, row in enumerate(puzzle_input):
        for c, cell in enumerate(row):
            if cell == "#":
                rocks.add((r, c))
            elif cell == "S":
                start = (r, c)

    return rocks, start, width, height


def BFS(rocks, start, width, height, steps, even=True):
    """Run a BFS on the grid to find the number of possible positions
    that can be reached within given number of steps.

    This could also mean that we just step back and forth multiple times."""
    seen = set()
    # dictionary: number of steps: [positions reached]
    reached_by_steps = defaultdict(set)
    # position, number of steps taken
    q = [(start, 0)]
    while q:
        curr_pos, curr_steps = q.pop(0)

        if curr_pos in seen:
            continue

        seen.add(curr_pos)
        reached_by_steps[curr_steps].add(curr_pos)

        # generate next steps
        for dr, dc in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
            next_pos = (curr_pos[0] + dr, curr_pos[1] + dc)
            if (
                0 <= next_pos[0] < height
                and 0 <= next_pos[1] < width
                and next_pos not in rocks
                and curr_steps + 1 <= steps
            ):
                q.append((next_pos, curr_steps + 1))

    # when we get here, we have evaluated all possible steps to reach each cell
    # while not going over the number of required steps
    # return the number of positions that can be reached in number of steps
    # this is determined by all possible positions that can be reached in an
    # even number of steps - as we can just step back and forth, so reach
    # the same position in 2, 4, 6, 8 etc steps
    step_remainder = 0 if even else 1
    all_positions = set()
    for x in reached_by_steps:
        if x % 2 == step_remainder:
            all_positions |= reached_by_steps[x]

    return len(all_positions)


# @aoc_timer
def part1(puzzle_input, steps):
    """Solve part 1. Return the required output value."""
    rocks, start, width, height = parse_grid(puzzle_input)
    result = BFS(rocks, start, width, height, steps)

    return result


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/21.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input, 64)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input, 26501365)
    print(f"Part 2: {p2}")

# Part 1: Start: 10:54 End: 11:31
# Part 2: Start: 11:32 End:
