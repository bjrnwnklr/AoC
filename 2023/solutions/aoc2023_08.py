# Load any required modules. Most commonly used:

import re
import math
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        return f.read().strip()


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    instr, lines = puzzle_input.split("\n\n")
    # parse the nodes
    regex = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")
    g = {}
    for line in lines.split("\n"):
        node, left, right = regex.findall(line.strip())[0]
        g[node] = (left, right)

    # iterate through instructions
    start = "AAA"
    end = "ZZZ"
    l = len(instr)
    step = 0
    q = [(start, step)]
    while q:
        curr, step = q.pop(0)
        if curr == end:
            break

        next_instr = instr[step % l]
        step += 1
        q.append((g[curr][0 if next_instr == "L" else 1], step))

    return step


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    instr, lines = puzzle_input.split("\n\n")
    # parse the nodes
    regex = re.compile(r"([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)")
    g = {}
    for line in lines.split("\n"):
        node, left, right = regex.findall(line.strip())[0]
        g[node] = (left, right)

    # find all nodes that end in 'A' and 'Z'
    aaas = []
    zzzs = []
    for n in g:
        if n[-1] == "A":
            aaas.append(n)
        elif n[-1] == "Z":
            zzzs.append(n)

    # each starting node likely has some periodicity after which
    # the nodes visited repeat.
    # store the path to any node end with Z in a dict with start and
    # end node to compare if we have taken the same path before
    seen = dict()
    for node_a in aaas:
        # iterate through instructions
        l = len(instr)
        step = 0
        path = node_a
        q = [(node_a, step, path)]
        while q:
            curr, step, curr_path = q.pop(0)
            if curr in zzzs:
                # add path to the seen dictionary
                seen[(node_a, curr)] = (curr_path, step)
                break

            next_instr = instr[step % l]
            step += 1
            next_node = g[curr][0 if next_instr == "L" else 1]
            q.append((next_node, step, path + next_node))

        # finished iterating for one node, lets get length of path

    # find the least common multiple of the steps required to reach
    # a node ending with Z
    result = math.lcm(*list(s[1] for s in seen.values()))

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/08.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 17:37 End: 17:55
# Part 2: Start: 17:58 End: 18:28

# Elapsed time to run part1: 0.00344 seconds.
# Part 1: 21251
# Elapsed time to run part2: 0.02172 seconds.
# Part 2: 11678319315857
