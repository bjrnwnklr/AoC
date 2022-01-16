# Load any required modules. Most commonly used:

# import re
import logging
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
import functools

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
    positions = [(str_pos, char)
                 for str_pos, char in enumerate(burrow) if char in 'ABCD']

    results = []
    for str_pos, char in positions:
        pos = room_pos(str_pos)
        match pos:
            case (0, _):
                # check if in a hallway - assume it can move
                results.append(str_pos)
            case (r, c):
                # if not in the hallway: if pod is in the wrong room, it will have to move in any case
                # path_from_room_free can then check if it can exit the room.
                target_room = ROOMS[char]
                if str_pos not in target_room:
                    # if not in the correct room the pod can possibly move
                    results.append(str_pos)
                else:
                    # if the pod is in the correct room, it still needs to move if the pods below are
                    # not in the right room
                    i = r
                    while i < len(target_room):
                        if burrow[target_room[i]] == char:
                            # next pod down is of the same type, i.e. in the correct room
                            i += 1
                        else:
                            results.append(str_pos)
                            break

    return results


def target_room_free(burrow: str, pod_type: str) -> tuple[bool, int]:
    """Return if the target room for a given pod type is free to move into, and if yes, 
    which position can be moved into (deepest row that is free). 

    Returns a tuple of (bool, int) = (True if room can be moved into, position that can be moved to).
    """
    target_room = ROOMS[pod_type]
    # go through each row of the room until we find an occupied on, or arrive at the bottom
    i = 0
    while i < len(target_room):
        # free room, move to next row
        if burrow[target_room[i]] == '.':
            i += 1
        else:
            # room is occupied, check if remaining slots are occupied by the correct pods
            # Room is only free if we are deeper than the first row (if we get to here and
            # are still on the first row, the room is completely full)
            if i > 0 and all(burrow[x] == pod_type for x in target_room[i:]):
                return (True, target_room[i - 1])
            else:
                return (False, -1)
    return (True, target_room[-1])


def path_from_room_free(burrow: str, pos_from: int) -> bool:
    """Return if the pod at given position can exit the room it is in."""
    # if the pod is in the hallway, the room is free by default
    if pos_from < 11:
        return True
    # check which row the pod is in
    row, _ = room_pos(pos_from)
    # check that all rows above are free
    if all(burrow[x] == '.' for x in (pos_from - i * 4 for i in range(1, row))):
        return True

    return False


@functools.cache
def room_pos(pos: int) -> tuple[int, int]:
    """Return the (row, column) tuple of a room, given it's index in a burrow string representation."""
    if pos < 11:
        # in hallway
        return (0, pos)
    else:
        row = ((pos - 11) // 4) + 1
        col = (((pos - 11) % 4) + 1) * 2
        return (row, col)


def hallway_free(burrow: str, pos_from: int, pos_to: int) -> bool:
    """Return if the hallway between two positions is free."""
    # get hallway position if pos_from is in a room
    col_from = room_pos(pos_from)[1]
    col_to = room_pos(pos_to)[1]
    if col_from < col_to:
        f = col_from + 1
        t = col_to
    else:
        f = col_to + 1
        t = col_from
    hallway = burrow[f:t]
    return hallway == '.' * (t - f)


@functools.cache
def path_length(pos_from: int, pos_to: int) -> int:
    """Calculate the number of steps required to get from pos_from to pos_to."""
    f = room_pos(pos_from)
    t = room_pos(pos_to)

    # if not in the same room, the number of steps is:
    #   row[f] + number of hallway steps between f and t + row[t]
    # if in the same room, the number of steps is:
    #   abs(row[f] - row[t])
    if f[1] != t[1]:
        return f[0] + abs(f[1] - t[1]) + t[0]
    else:
        return abs(f[0] - t[0])


def path_cost(steps: int, p_type: str) -> int:
    """Return the cost of moving a pod of the provided type by the number of steps."""
    return steps * COST[p_type]


def possible_moves(burrow: str, pos_from: int) -> list[tuple[int, int]]:
    """Return all possible moves as a list of tuples (cost, position_to_move_to)
    for a pod at a given position (pos_from) in the burrow.
    """
    locations_to = []
    # get the type of the pod and the location in (row, col) notation
    p_type = burrow[pos_from]

    # Default case: the pod should move to the target room if possible, regardless if in
    # the hallway or in a room.
    # - check if the target room is free
    # - check if the hallway path is clear and if the pod can move from the room
    target_free, target_pos = target_room_free(burrow, p_type)
    if target_free and hallway_free(burrow, pos_from, target_pos) and path_from_room_free(burrow, pos_from):
        locations_to.append(target_pos)
    else:
        # Otherwise, the pod can move to a hallway position if it is in a room and can move out of the room
        if pos_from > 10 and path_from_room_free(burrow, pos_from):
            for loc in [0, 1, 3, 5, 7, 9, 10]:
                if (burrow[loc] == '.' and
                        hallway_free(burrow, pos_from, loc)):
                    locations_to.append(loc)

    # calculate the cost for each step
    results = []
    for pos_to in locations_to:
        steps = path_length(pos_from, pos_to)
        cost = path_cost(steps, p_type)
        results.append((cost, pos_to))

    return results


def move_to(burrow: str, pos_from: int, pos_to: int) -> str:
    """Perform a move of a pod from / to and return the new state of the burrow as a string."""
    b = list(burrow)
    b[pos_to], b[pos_from] = b[pos_from], b[pos_to]
    return ''.join(b)


def heuristic(burrow: str) -> int:
    """Returns the sum of horizontal move cost for all pods not in the correct room."""
    # find all characters and their positions
    positions = [(str_pos, char)
                 for str_pos, char in enumerate(burrow) if char in 'ABCD']

    result = 0
    for str_pos, char in positions:
        # get column position for pod and the target room for the pod
        # using the first entry of the rooms for pod type
        _, col_from = room_pos(str_pos)
        _, col_to = room_pos(ROOMS[char][0])
        result += COST[char] * abs(col_from - col_to)

    return result


def dijkstra(start: str, target: str) -> int:
    """Run a Dijkstra search for the cheapest path from start to target.

    Return the cost of the path.
    """

    # queue = state of the burrow (which includes the cost)
    q = [(0, start)]
    seen = set()
    distances = defaultdict(lambda: 1e09)
    paths = defaultdict(list)
    steps = 0
    while q:
        cur_cost, cur_state = heappop(q)
        steps += 1
        # logging.debug(
        #     f'Dijkstra: {steps=} {cur_cost=} {cur_state=}')

        # if already seen, discard
        if cur_state in seen:
            continue

        seen.add(cur_state)

        # if we found the target, we're done
        if cur_state == target:
            print(f'Target reached: {cur_state}, cost {cur_cost}.')
            print(f'Target path: {paths[target]}')
            print(f'Number of states processed: {steps=}')
            # logging.info(
            #     f'Target reached: {cur_state}, cost {cur_cost}.')
            # logging.info(f'Target path: {paths[target]}')
            # logging.info(f'Number of states processed: {steps=}')
            return distances[target]

        # get a list of all possible movers...
        for p in movers(cur_state):
            # ...and their possible moves
            for inc_cost, move_loc in possible_moves(cur_state, p):
                next_move = move_to(cur_state, p, move_loc)
                next_cost = cur_cost + inc_cost
                if next_move not in seen and next_cost < distances[next_move]:
                    distances[next_move] = next_cost
                    paths[next_move] = paths[cur_state] + [next_move]
                    heappush(q, (next_cost, next_move))

    # logging.info(f'Target path: {paths[target]}')
    return distances[target]


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    start = to_string(puzzle_input)
    target = to_string(['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'])

    # # run the dijkstra search to find the shortest path
    cost = dijkstra(start, target)

    return cost


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, filename="23_reduced_steps.log")

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
