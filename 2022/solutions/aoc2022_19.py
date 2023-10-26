# Load any required modules. Most commonly used:

import re

# from collections import deque
from copy import deepcopy

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

    def signature(self):
        """Returns tuple of (minute, robots). Can
        be used as a key in a dictionary."""
        return (self.minute, *self.robots)

    def __repr__(self):
        return (
            f"State: minute {self.minute}, robots: {self.robots},"
            + f" materials: {self.materials}"
        )


def score(state, blueprint):
    """Returns the cost of a state's materials based
    on ore and minutes spent to produce.

    Score(x) = (ore_for_robot + minutes to produce x materials)
    E.g. if blueprint is
    - ore robot: 4 ore
    - clay robot: 2 ore
    then score for 1 ore + 1 clay is
    (4 + 1) + (2 + 1)
    """

    def ore(n):
        if n > 0:
            return blueprint[1] + n
        else:
            return 0

    def clay(n):
        if n > 0:
            return ore(blueprint[2]) + n
            # return blueprint[2] + n
        else:
            return 0

    def obsidian(n):
        if n > 0:
            return blueprint[3] + clay(blueprint[4]) + n
        else:
            return 0

    def geode(n):
        if n > 0:
            return blueprint[5] + obsidian(blueprint[6]) + n
        else:
            return 0

    # ore = ore, consider just using the materials as we start with one
    # ore bot?
    result = (
        ore(state.materials[0])
        + clay(state.materials[1])
        + obsidian(state.materials[2])
        + geode(state.materials[3])
    )
    return result


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
        print()
        # brute force it - evaluate all options
        # we can then try to find scenarios that reduce
        # the solution space
        q = [State()]
        print(f"Starting to process blueprint {blueprint}")
        finished_states = []
        while q:

            curr = q.pop(0)
            # print(f"Popped {curr} from queue.")
            # print(f"Seen this state already: {not_seen(curr, state_register)}")

            # check if minute is 24
            if curr.minute == MINUTES:
                # time is up for this state, break and store the current state
                # print(f"Finished at minute {curr.minute}: state {curr}")
                finished_states.append(curr)
                continue

            # work through purchasing options
            # this will get messy as purchasing the cheapest option will always come first
            # states are the same if the same number of robots and materials are detected
            # for the same minute

            # add one new state to the production queue, as this is
            # the default action: do not purchase, just collect whatever is possible
            production = [(-1, deepcopy(curr))]
            # try all purchasing options - we can only purchase one robot per round
            for m in range(4):
                # create another new state, which will only get added if
                # a new robot can be produced
                new_state = deepcopy(curr)
                match m:
                    case 0:
                        # ore robot, costs x ore
                        if new_state.materials[0] >= blueprint[1]:
                            production.append((0, new_state))
                            new_state.materials[0] -= blueprint[1]
                            # print(f"\t Can afford an ore robot, buying.")
                    case 1:
                        # clay robot, costs x ore
                        if new_state.materials[0] >= blueprint[2]:
                            production.append((1, new_state))
                            new_state.materials[0] -= blueprint[2]
                            # print(f"\t Can afford a clay robot, buying.")
                    case 2:
                        # obsidian robot, costs x ore and y clay
                        if (
                            new_state.materials[0] >= blueprint[3]
                            and new_state.materials[1] >= blueprint[4]
                        ):
                            production.append((2, new_state))
                            new_state.materials[0] -= blueprint[3]
                            new_state.materials[1] -= blueprint[4]
                            # print(f"\t Can afford an obsidian robot, buying.")
                    case 3:
                        # geode robot, costs x ore and y obsidian
                        if (
                            new_state.materials[0] >= blueprint[5]
                            and new_state.materials[2] >= blueprint[6]
                        ):
                            production.append((3, new_state))
                            new_state.materials[0] -= blueprint[5]
                            new_state.materials[2] -= blueprint[6]
                            # print(f"\t Can afford a geode robot, buying.")

            # process all purchases and add new states to the queue
            for robot_to_purchase, next_state in production:
                # print(
                #     f"\t Purchasing {robot_to_purchase}, "
                #     + f"creating a new state {next_state}"
                # )

                # produce any material
                for m in range(4):
                    next_state.materials[m] += next_state.robots[m]

                # lastly, production finishes, add robot to list
                if robot_to_purchase >= 0:
                    next_state.robots[robot_to_purchase] += 1

                # add new state to queue and increase minute
                next_state.minute += 1

                # PRUNING of the queue
                # go through queue and remove any states that have already been seen
                temp_queue = q[:]
                q = []
                max_state = deepcopy(next_state)
                for t in temp_queue:
                    if t.signature() == next_state.signature():
                        # print(
                        #     "Found same signature in queue: \n"
                        #     + f"\t {t=}\n"
                        #     + f"\t {next_state=}\n"
                        #     + f"\t {max_state=}"
                        # )
                        if score(max_state, blueprint) <= score(t, blueprint):
                            # found that an existing entry in the queue is higher
                            # than the current state, so keep the t entry from the queue
                            # as new max
                            max_state = deepcopy(t)
                            # debug to see what happens here
                            # print(
                            #     f"max state: {max_state} <= {t}, next_state {next_state}, "
                            # )
                    else:
                        # t is not the same state as next, so add back to queue
                        q.append(t)
                # append next state or highest state with same signature (already in the queue)
                q.append(max_state)

            # print current queue
            # print(f"Current queue: {q}")
        # done with processing queue, evaluate largest geode output
        highest_geodes = max(finished_states, key=lambda x: x.materials[3])
        print(f"Finished processing blueprint, highest geodes in {highest_geodes}")

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
