# Load any required modules. Most commonly used:

import re

from collections import deque
from math import ceil

# from utils.aoctools import aoc_timer
# from dataclasses import dataclass

MINUTES = 24


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


def state_hash(state):
    """Return a comparable hash of a state consisting of
    (minute, [robots], [materials]).
    """
    return (state[0], *state[1], *state[2])


def produce(state, minutes):
    """Return an updated state that has all materials
    that will be produced by the robots in the number of
    minutes provided. Minutes is updated to current minutes
    plus the minutes provided.
    """
    return (
        minutes + state[0],
        state[1][:],
        [m + r * minutes for r, m in zip(state[1], state[2])],
    )


def recipes(blueprint):
    """Returns a dictionary of recipes for a robot:

    robot to build: [materials required] e.g.
    ore:
    0: [4, 0, 0, 0]
    geode:
    3: [2, 0, 7, 0]
    """
    d = dict()
    d[0] = [blueprint[1], 0, 0, 0]
    d[1] = [blueprint[2], 0, 0, 0]
    d[2] = [blueprint[3], blueprint[4], 0, 0]
    d[3] = [blueprint[5], 0, blueprint[6], 0]
    return d


def minutes_to_build(recipe, state, robot):
    """Calculates the number of minutes required to build a robot given
    the current robots and materials, based on the recipe in the blueprint.
    Returns the number of minutes required to mine any missing materials plus
    the 1 minute to build."""
    # fail if robots required to build are not available
    assert all(state[1][r] > 0 for r, m in enumerate(recipe[robot]) if m > 0)
    return (
        max(
            max(
                0,
                ceil((r - state[2][m]) / state[1][m]),
            )
            for m, r in enumerate(recipe[robot])
            if r > 0  # only process recipe elements if required
        )
        + 1
    )


def bfs(blueprint, minutes):
    """Run a BFS across all states that are possible.
    Transitions / states are what robots can be bought next, plus
    one default state that just continues producing materials
    with the existing robots until time (minutes) is reached.

    Returns the state with the highest number of geodes found
    after minutes have passed.
    """
    # generate a reusable recipe from the blueprint
    recipe = recipes(blueprint)
    # calculate max materials required for any robot
    max_materials = [max(r[i] for r in recipe.values()) for i in range(4)]
    seen = set()
    # minutes, robots, materials
    start = (0, [1, 0, 0, 0], [0, 0, 0, 0])
    highest_geode_state = start
    q = deque([start])
    while q:
        # next element
        curr_state = q.popleft()
        # print(f"BFS evaluation {curr_state}")

        # proceed only if we have not seen the current state
        if state_hash(curr_state) in seen:
            continue

        # add current state to seen so we don't process it again
        seen.add(state_hash(curr_state))

        # if we have reached the maximum minutes, check
        # if the current state has a higher number of geodes produced
        # than previous states
        if curr_state[0] == minutes:
            # print(f"Minute {minutes} reached, {curr_state}")
            if curr_state[2][3] > highest_geode_state[2][3]:
                highest_geode_state = curr_state
            continue

        # process next states
        # each state is either
        # - the next robot that can be bought with the current materials and
        #   robots (i.e. we can only build a robot where we have the robots that
        #   are required to mine the materials required for the robot). The minute
        #   is set to the time required to mine the required materials and build
        #   the robot (i.e. +1).
        # - a default where we do not purchase any further robots and just mine
        #   materials with existing robots for the remaining time

        # Default state
        # optimization: only add if number of geodes is higher than
        # current max
        default_state = produce(curr_state, minutes - curr_state[0])
        if default_state[2][3] > highest_geode_state[2][3]:
            q.append(default_state)

        # assess which robots can be built in which time and
        # add them to the queue
        for robot in range(4):
            # print(f"Checking if we can produce robot {robot} from {curr_state}")
            # optimization - brings massive speed increase:
            # only build ore, clay or obsidian bots if we have less bots
            # than we can spend in 1 minute (doesn't work for geodes as
            # there is no spend per minute on geodes)
            if robot < 3 and curr_state[1][robot] > max_materials[robot]:
                continue
            # only create a robot if we have the robots to produce materials
            # we don't need to check if we have enough materials, as that is
            # calculated as part of the minutes_to_build function
            # and we wouldnt have any relevant materials if we didnt have the
            # corresponding robots
            if all(curr_state[1][r] > 0 for r, m in enumerate(recipe[robot]) if m > 0):
                # calculate the number of minutes required to build
                # based on existing materials
                m = minutes_to_build(recipe, curr_state, robot)
                # create a new state
                new_minute = curr_state[0] + m
                # only produce robots if the minute is less than the target minute
                if new_minute < minutes:
                    new_robots = curr_state[1][:]
                    # add any materials produced during the time (including one minute to
                    # produce robot as we continue to produce materials during that minute)
                    # and remove any materials spent on the new robot
                    new_materials = [
                        (m * new_robots[i]) + curr_state[2][i] - recipe[robot][i]
                        for i in range(4)
                    ]
                    # create new robot
                    new_robots[robot] += 1
                    # add new robot to the queue
                    # print(
                    #     f"Produced new robot ({new_minute}, {new_robots}, {new_materials})"
                    # )
                    q.append((new_minute, new_robots, new_materials))

    # once all states have been evaluated and q is empty, return
    # the state with the highest geode count
    return highest_geode_state


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    Multiply blueprint ID with largest number of geodes that can be
    opened in 24 minutes. Add up all these products.

    Run a BFS for each blueprint.
    State of a BFS is
    """
    # each blueprint is returned as a list of numbers
    # ore robot costs x ore
    # clay robot costs x ore
    # obsidian robot costs x ore and y clay
    # geode robot costs x ore and y obsidian
    result = 0
    for blueprint in puzzle_input:
        print()
        print(f"Evaluating blueprint: {blueprint}")
        highest_geode_state = bfs(blueprint, MINUTES)
        print(f"Highest geode count for state: {highest_geode_state}")
        result += blueprint[0] * highest_geode_state[2][3]

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
