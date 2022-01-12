# Load any required modules. Most commonly used:

# import re
import logging
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush

from utils.aoctools import aoc_timer

COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

TARGET_ROOM = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        lines = f.readlines()
        for line in lines[2:4]:
            pods = list(line.strip().replace('#', ''))
            puzzle_input.extend(pods)

    return puzzle_input


def dijkstra(start: Burrow, target: Burrow) -> int:
    """Run a Dijkstra search for the cheapest path from start to target.

    Return the cost of the path.
    """

    # queue = state of the burrow (which includes the cost)
    q = [start]
    seen = set()
    distances = defaultdict(lambda: 1e09)
    paths = defaultdict(list)
    steps = 0
    while q:
        cur_state = heappop(q)
        steps += 1
        logging.debug(
            f'Dijkstra: {steps=} {cur_state.cost=} {cur_state.state()}')

        # if already seen, discard
        if cur_state.state() in seen:
            continue

        seen.add(cur_state.state())

        # if we found the target, we're done
        if cur_state.state() == target.state():
            logging.info(
                f'Target reached: {cur_state.state()}, cost {cur_state.cost}.')
            logging.info(f'Target path: {paths[target.state()]}')
            logging.info(f'Number of states processed: {steps=}')
            return distances[target.state()]

        for pid, inc_cost, move_loc in cur_state.possible_moves():
            next_move = cur_state.move_copy(pid, inc_cost, move_loc)
            if next_move.state() not in seen and next_move.cost < distances[next_move.state()]:
                distances[next_move.state()] = next_move.cost
                paths[next_move.state()] = paths[cur_state.state()] + \
                    [next_move.state()]
                heappush(q, next_move)

    logging.info(f'Target path: {paths[target.state()]}')
    return distances[target.state()]


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    start = Burrow(puzzle_input)
    target = Burrow(['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'])

    # run the dijkstra search to find the shortest path
    cost = dijkstra(start, target)

    return cost


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # read the puzzle input
    puzzle_input = load_input('input/23.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 14:15 End:
# Part 2: Start:  End:

"""
First attempt at part 1 with Dijkstra: 15542 - answer is too high:

Elapsed time to run part1: 0.50177 seconds.
Part 1: 15542

Correct solution is 15516 as per another solution.

INFO:root:Target reached: (19536, '...........ABCDABCD'), cost 19536.
INFO:root:Target reached: (15516, '...........ABCDABCD'), cost 15516.
INFO:root:Target path: ['A..........D.BCBADC', 'AA.........D.BCB.DC', 'AA.........D..CBBDC', 'AA.......C.D...BBDC', 'AA...C...C.D...BBD.', 'AA...C...C.D...BB.D', 'AA.......C.D...BBCD', 'AA.........D.C.BBCD', 'AA...........CDBBCD', 'AA..........BCD.BCD', 'A...........BCDABCD', '...........ABCDABCD']
Elapsed time to run part1: 2.46506 seconds.
Part 1: 15516
Part 2: 1
"""
