# Load any required modules. Most commonly used:

import re
from collections import defaultdict
from operator import lt, gt

from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = f.read()

    return puzzle_input


def parse_input(puzzle_input):
    """Breaks the input into two lists:
    - workflows
    - parts
    """
    workflows_raw, parts_raw = puzzle_input.strip().split("\n\n")
    # generate a dictionary of workflows
    # key: workflow name
    # value: list of the workflow rules
    workflows = defaultdict(list)
    for line in workflows_raw.split("\n"):
        wf_name, rules = line.split("{")
        rules = rules.strip("}")
        for r in rules.split(","):
            if ":" in r:
                cond, dest = r.split(":")
                # condition is always 1 letter, < or >, integer
                cat, comp, thresh = cond[0], cond[1], int(cond[2:])
                workflows[wf_name].append((cat, comp, thresh, dest))
            else:
                # default rule, just append it raw
                workflows[wf_name].append((r))

    # generate a list of dictionaries with x, m, a, s keys
    parts = []
    regex = re.compile(r"(\d+)")
    for line in parts_raw.split("\n"):
        matches = regex.findall(line)
        if matches:
            parts.append(
                {k: v for k, v in zip(["x", "m", "a", "s"], list(map(int, matches)))}
            )

    return workflows, parts


def process(part, flow, workflows) -> int:
    """Recursive processing of part part through the workflows, starting
    with the workflow named `flow`.

    Returns the sum of the ratings if the part is accepted, or 0 if rejected."""
    if flow == "A":
        return sum(part.values())
    elif flow == "R":
        return 0
    # process flow
    f = workflows[flow]
    for rule in f[:-1]:
        # a rule to process
        cat, comp, thresh, dest = rule
        if comp == "<":
            op = lt
        else:
            op = gt
        if op(part[cat], thresh):
            return process(part, dest, workflows)

    # default rule, process if we get to this point
    return process(part, f[-1], workflows)


def process_2(part, flow, workflows) -> int:
    """Recursive processing of part part through the workflows, starting
    with the workflow named `flow`.

    For part 2, the parts represent a dictionary of intervals that
    are valid to get through to the next flow.
    e.g. {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}

    Returns the sum of the ratings if the part is accepted, or 0 if rejected."""
    if flow == "A":
        # accepted result, return the product of the
        # lengths of the accepted ranges
        result = 1
        # part consists of intervals [a, b] for each x, m, a, s key
        for a, b in part.values():
            result *= b - a + 1
        return result
    elif flow == "R":
        # rejected result, this group of intervals does
        # not contribute to the possible values, so return 0
        return 0
    # process flow
    f = workflows[flow]
    result = 0
    for rule in f[:-1]:
        # a rule to process
        cat, comp, thresh, dest = rule
        if comp == "<":
            op = lt
        else:
            op = gt
        # a is lower bound, b is upper bound of valid values for
        # cat (x, m, a, s)
        a, b = part[cat]
        # split the interval
        if op(a, thresh) and op(b, thresh):
            # both bounds meet the condition, so
            # just pass the interval on to the destination
            # Return here since we don't need to process any other
            # rules of the workflow
            return process_2(part.copy(), dest, workflows)
        elif not op(a, thresh) and not op(b, thresh):
            # both bounds don't meet the condition, so
            # pass on the intervall unchanged to the next rule
            continue
        elif op(a, thresh) and not op(b, thresh):
            # op is lt, a < thresh < b
            # pass on [a:thresh-1] to dest, move [thresh:b] to next rule in flow
            passed = part.copy()
            passed[cat] = (a, thresh - 1)
            part[cat] = (thresh, b)
            result += process_2(passed, dest, workflows)
        elif not op(a, thresh) and op(b, thresh):
            # op is gt, a < thresh < b
            # pass on [thresh + 1:b] to dest, move [a:thresh] to next rule in flow
            passed = part.copy()
            passed[cat] = (thresh + 1, b)
            part[cat] = (a, thresh)
            result += process_2(passed, dest, workflows)

    # default
    result += process_2(part.copy(), f[-1], workflows)

    return result


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    workflows, parts = parse_input(puzzle_input)

    # process all parts through the 'in' workflow until either accepted or rejected
    result = 0
    for p in parts:
        result += process(p, "in", workflows)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    workflows, _ = parse_input(puzzle_input)
    result = process_2(
        {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)},
        "in",
        workflows,
    )

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/19.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 14:28 End: 15:30
# Part 2: Start: 15:35 End: 16:34

# Elapsed time to run part1: 0.00157 seconds.
# Part 1: 449531
# Elapsed time to run part2: 0.00176 seconds.
# Part 2: 122756210763577
