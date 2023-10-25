# Load any required modules. Most commonly used:

import re

from collections import deque, defaultdict
from copy import deepcopy

# from utils.aoctools import aoc_timer
# from dataclasses import dataclass

MINUTES = 2


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    regex = re.compile(r"(\d+)")

    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            matches = regex.findall(line.strip())
            if matches:
                puzzle_input.append(list(map(int, matches)))

    return puzzle_input


class State:
    def __init__(self):
        # number of ore, clay, obsidian, geode robots
        self.robots = [1, 0, 0, 0]
        # number of collected ore, clay, obsidian, geode materials
        self.materials = [0, 0, 0, 0]
        # minute
        self.minute = 0
        # the path taken to this solution
        # this is a list of States appended to a list
        # self.path = []

    def __repr__(self):
        return (
            f"State: minute {self.minute}, robots: {self.robots},"
            + f" materials: {self.materials}"
        )


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    Multiply blueprint ID with largest number of geodes that can be
    opened in 24 minutes. Add up all these products.

    Run a BFS for each blueprint.
    State of a BFS is
    - minute
    - number of robots of each type
    - number of ore and clay and obsidian collected
    - number of geodes opened

    Possible optimization:
    - consider same state if number of robots is same for the minute
      and discard if number of ore, clay, obsidian and geodes is larger
    - or, total number of ore, clay and obsidian (incl spent on robots)
      and geodes opened is larger for the same minute (regardless of number
      of robots i.e. how it was spent)
    """
    # each blueprint is returned as a list of numbers
    # ore robot costs x ore
    # clay robot costs x ore
    # obsidian robot costs x ore and y clay
    # geode robot costs x ore and y obsidian
    for blueprint in puzzle_input:
        # brute force it - evaluate all options
        # we can then try to find scenarios that reduce
        # the solution space
        q = deque([State()])
        state_max_geodes = State()
        while q:

            curr = q.popleft()
            # check if minute is 24
            if curr.minute == MINUTES:
                # time is up for this state, break and store the current state
                if curr.materials[3] > state_max_geodes.materials[3]:
                    print(f"Finished at minute {curr.minute}: state {curr}")
                    state_max_geodes = curr
                break

            # work through purchasing options
            # this will get messy as purchasing the cheapest option will always come first
            # states are the same if the same number of robots and materials are detected
            # for the same minute
            # robots to purchase: ore, clay, obsidian, geode
            production = [-1]
            for m in range(4):
                to_purchase = (
                    -1
                )  # purchase nothing (-1), or purchase a robot represented by m
                match m:
                    case 0:
                        # ore robot, costs x ore
                        if curr.materials[0] >= blueprint[0]:
                            production.append(0)
                            curr.materials[0] -= blueprint[0]
                    case 1:
                        # clay robot, costs x ore
                        if curr.materials[0] >= blueprint[1]:
                            production.append(1)
                            curr.materials[0] -= blueprint[0]
                    case 2:
                        # obsidian robot, costs x ore and y clay
                        if (
                            curr.materials[0] >= blueprint[2]
                            and curr.materials[1] >= blueprint[3]
                        ):
                            production.append(2)
                            curr.materials[0] -= blueprint[2]
                            curr.materials[1] -= blueprint[3]
                    case 3:
                        # geode robot, costs x ore and y obsidian
                        if (
                            curr.materials[0] >= blueprint[4]
                            and curr.materials[2] >= blueprint[5]
                        ):
                            production.append(3)
                            curr.materials[0] -= blueprint[4]
                            curr.materials[2] -= blueprint[5]

            for s in production:
                # create new state
                new_state = deepcopy(curr)

                # produce any material
                for m in range(4):
                    new_state.materials[m] += new_state.robots[m]

                # lastly, production finishes, add robot to list
                if s >= 0:
                    new_state.robots[s] += 1

                # add new state to queue and increase minute
                new_state.minute += 1
                q.append(new_state)

            # print current queue
            print(f"Current queue: {q}")

    return 1


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/19.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 17:00 End:
# Part 2: Start:  End:
