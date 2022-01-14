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


HALLWAY = list(range(11))

ROWS = {
    1: list(range(11, 15)),
    2: list(range(15, 19))
}

ROOMS = {
    'A': [11, 15],
    'B': [12, 16],
    'C': [13, 17],
    'D': [14, 18]
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


def to_string(puzzle_input: list[str]) -> str:
    """Convert the puzzle input list (a list of 8 characters, representing the 4 rooms of the
    puzzle) into a string with the format '............ABCDABCD', representing the hallway
    and 4 rooms.
    """
    return '.' * 11 + ''.join(puzzle_input)


def movers(burrow: str) -> list[int]:
    """Analyze a burrow string representation and generate a list of pods (identified by their
    position in the string) who can move."""
    # find all characters and their positions
    positions = [(pos, char)
                 for pos, char in enumerate(burrow) if char in 'ABCD']

    results = []
    for pos, char in positions:
        match pos:
            case pos if pos in HALLWAY:
                # check if in a hallway - assume it can move
                results.append((pos, char))
            case pos if pos in ROWS[1]:
                target_room = ROOMS[char]
                if pos not in target_room:
                    # if in the first row of a wrong room, we can move
                    results.append((pos, char))
                else:
                    # if the pod is in the correct room, it still needs to move if the pod below is
                    # not in the right room
                    lower_pod = burrow[pos + 4]
                    if (pos + 4) not in ROOMS[lower_pod]:
                        results.append((pos, char))
            case pos if pos in ROWS[2]:
                target_room = ROOMS[char]
                if pos not in target_room and burrow[pos - 4] == '.':
                    results.append((pos, char))

    return results


def target_room_free(burrow: str, pod_type: str) -> tuple[bool, int]:
    """Return if the target room for a given pod type is free to move into, and if yes, 
    which position can be moved into (deepest row that is free). 

    Returns a tuple of (bool, int) = (True if room can be moved into, position that can be moved to).
    """
    target_room = ROOMS[pod_type]
    # check if all positions are occupied
    if all(burrow[x] != '.' for x in target_room):
        return (False, -1)
    # check if all positions are empty
    if all(burrow[x] == '.' for x in target_room):
        return (True, max(target_room))
    # if not all rows are free, go from top down and check if occupied rows have correct pod type
    i = 0
    while i < len(target_room):
        if burrow[target_room[i]] == '.':
            i += 1
        else:
            # room is occupied, check if remaining slots are occupied by the correct pods
            if all(burrow[x] == pod_type for x in target_room[i:]):
                return (True, target_room[i - 1])
            else:
                return (False, -1)


def path_from_room_free(burrow: str, pos_from: int) -> bool:
    """Return if the pod at given position can exit the room it is in."""
    # check which row the pod is in
    pod_row = (pos_from - 10) // 4
    # if it is in the first row (0 indexed in this case), it can exit
    if pod_row == 0:
        return True
    # otherwise, check that all rows above are free
    if all(burrow[x] == '.' for x in (pos_from - i * 4 for i in range(1, pod_row + 1))):
        return True

    return False


def possible_moves(burrow: str, pos_from: int) -> list[tuple[int, int]]:
    """Return all possible moves as a list of tuples (cost, position_to_move_to)
    for a pod at a given position (pos_from) in the burrow.
    """
    # get the type of the pod
    p_type = burrow[pos_from]

    # check if the pod can move to the target room
    # 1) where is the target room
    target_room = ROOMS[p_type]
    # 2) is the target room free (if both slots empty, or if slot 2 has the correct pod)

    return [(0, 0)]


# def dijkstra(start: Burrow, target: Burrow) -> int:
#     """Run a Dijkstra search for the cheapest path from start to target.

#     Return the cost of the path.
#     """

#     # queue = state of the burrow (which includes the cost)
#     q = [start]
#     seen = set()
#     distances = defaultdict(lambda: 1e09)
#     paths = defaultdict(list)
#     steps = 0
#     while q:
#         cur_state = heappop(q)
#         steps += 1
#         logging.debug(
#             f'Dijkstra: {steps=} {cur_state.cost=} {cur_state.state()}')

#         # if already seen, discard
#         if cur_state.state() in seen:
#             continue

#         seen.add(cur_state.state())

#         # if we found the target, we're done
#         if cur_state.state() == target.state():
#             logging.info(
#                 f'Target reached: {cur_state.state()}, cost {cur_state.cost}.')
#             logging.info(f'Target path: {paths[target.state()]}')
#             logging.info(f'Number of states processed: {steps=}')
#             return distances[target.state()]

#         for pid, inc_cost, move_loc in cur_state.possible_moves():
#             next_move = cur_state.move_copy(pid, inc_cost, move_loc)
#             if next_move.state() not in seen and next_move.cost < distances[next_move.state()]:
#                 distances[next_move.state()] = next_move.cost
#                 paths[next_move.state()] = paths[cur_state.state()] + \
#                     [next_move.state()]
#                 heappush(q, next_move)

#     logging.info(f'Target path: {paths[target.state()]}')
#     return distances[target.state()]


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    # start = Burrow(puzzle_input)
    # target = Burrow(['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'])

    # # run the dijkstra search to find the shortest path
    # cost = dijkstra(start, target)

    return 1


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
