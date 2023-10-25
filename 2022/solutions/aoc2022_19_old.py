# Load any required modules. Most commonly used:

import re

from collections import deque, defaultdict

# from utils.aoctools import aoc_timer
from dataclasses import dataclass, replace


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


@dataclass
class State:
    minute: int = 1
    a_ore: int = 0
    a_clay: int = 0
    a_obs: int = 0
    t_ore: int = 0
    t_clay: int = 0
    t_obs: int = 0
    a_geode: int = 0
    r_ore: int = 1
    r_clay: int = 0
    r_obs: int = 0
    r_geode: int = 0

    def __hash__(self) -> int:
        return hash(
            (
                self.minute,
                self.a_ore,
                self.a_clay,
                self.a_obs,
                self.a_geode,
                self.r_ore,
                self.r_clay,
                self.r_obs,
                self.r_geode,
            )
        )


class Blueprint:
    def __init__(self, recipe) -> None:
        self.id = recipe[0]
        # (ore, clay, obsidian)
        self.robots = {
            "ore": (recipe[1], 0, 0),
            "clay": (recipe[2], 0, 0),
            "obs": (recipe[3], recipe[4], 0),
            "geode": (recipe[5], 0, recipe[6]),
            "none": (0, 0, 0),
        }


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
    result = 0
    for blueprint in puzzle_input:
        bp = Blueprint(blueprint)
        print(f"Processing blueprint {bp.id}")

        max_geodes = 0

        q = deque([State()])
        seen = set()

        while q:
            curr = q.popleft()
            print(f"Popped {curr=}")
            if curr in seen:
                continue

            # get max number of geodes
            max_geodes = max(max_geodes, curr.a_geode)

            # process one round
            # start construction of any possible robots
            # these are the valid neighbours
            for robot in bp.robots:
                new_robot = False
                # create a copy of the current state
                next_state = replace(curr)
                # check if we have the resources
                if (
                    next_state.a_ore >= bp.robots[robot][0]
                    and next_state.a_clay >= bp.robots[robot][1]
                    and next_state.a_obs >= bp.robots[robot][2]
                ):
                    print(f"\tAdding robot {robot}")
                    # spend the resources
                    next_state.a_ore -= bp.robots[robot][0]
                    next_state.a_clay -= bp.robots[robot][1]
                    next_state.a_obs -= bp.robots[robot][2]
                    new_robot = True
                # collect resources
                next_state.a_ore += next_state.r_ore
                next_state.a_clay += next_state.r_clay
                next_state.a_obs += next_state.r_obs
                next_state.a_geode += next_state.r_geode

                # add new robots
                if new_robot:
                    match robot:
                        case "ore":
                            next_state.r_ore += 1
                        case "clay":
                            next_state.r_clay += 1
                        case "obs":
                            next_state.r_obs += 1
                        case "geode":
                            next_state.r_geode += 1

                # increase minute and add to queue
                next_state.minute += 1

                # add to queue if we still have time
                if next_state.minute <= 10:
                    q.append(next_state)
                    print(f"\tAppended {next_state}, q has {len(q)} elements")

        # BFS finished, calculate result
        result += bp.id * max_geodes
        print(f"Blueprint {bp.id} finished. {max_geodes=}, {result=}")

    return result


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
