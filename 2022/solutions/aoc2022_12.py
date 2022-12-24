# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer
from dataclasses import dataclass


@dataclass
class Node:
    row: int = 0
    col: int = 0
    height: int = 0


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        grid = {}
        end = Node()
        for r, line in enumerate(f.readlines()):
            for c, n in enumerate(line.strip()):
                if n == "S":
                    start = (r, c)
                    grid[(r, c)] = Node(r, c, 0)
                elif n == "E":
                    end = (r, c)
                    grid[(r, c)] = Node(r, c, 25)
                else:
                    grid[(r, c)] = Node(r, c, ord(n) - ord("a"))

    return grid, start, end


def neighbors(pos, grid):
    """Return all valid neighbor nodes"""
    result = []
    r, c = pos
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        rr = r + dr
        cc = c + dc
        if (rr, cc) in grid and grid[(rr, cc)].height - grid[(r, c)].height <= 1:
            result.append((rr, cc))

    return result


def BFS(grid, start, end):
    q = [(start, 0)]
    seen = set()

    while q:
        curr, steps = q.pop(0)

        if curr in seen:
            continue

        seen.add(curr)

        if curr == end:
            # found the end, return number of steps
            return steps

        for n in neighbors(curr, grid):
            if n not in seen:
                q.append((n, steps + 1))


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    grid, start, end = puzzle_input
    result = BFS(grid, start, end)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    grid, _, end = puzzle_input
    low_points = [n for n in grid if grid[n].height == 0]
    result = 10_000
    for start in low_points:
        steps = BFS(grid, start, end)
        if steps:
            result = min(result, steps)

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

# Part 1: Start:  End:
# Part 2: Start: 12:10 End: 12:18

# Elapsed time to run part1: 0.01336 seconds.
# Part 1: 339
# Elapsed time to run part2: 1.18422 seconds.
# Part 2: 332
