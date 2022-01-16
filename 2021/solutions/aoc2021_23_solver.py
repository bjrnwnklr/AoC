# Load any required modules. Most commonly used:

# import re
import logging
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import product

from utils.aoctools import aoc_timer


class Solver:
    """Generates the burrow based on number of rows in the rooms and provides solver functions to 
    solve the puzzle.

    Using this class provides an elegant way to generate burrows of varying depth without having to 
    change any of the other functions.
    """
    COST = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000
    }

    HALLWAY = list(range(11))

    def __init__(self, depth: int = 2) -> None:
        """Generates a solver instance based on a burrow of the provided depth."""
        self.depth = depth
        self.length = 11 + 4 * depth
        self.ROOMS = {
            r: list(range(start, start + self.depth * 4, 4))
            for r, start in zip('ABCD', range(11, 15))
        }
        # pre-calculate all translations of string index to (r, c) coordinates
        self.positions = {
            i: self._room_pos(i) for i in range(self.length + 1)
        }

        # pre-calculate all distances between two string indexes
        self.distances = {}
        for a, b in product(range(self.length + 1), repeat=2):
            self.distances[(a, b)] = self._path_length(a, b)
            self.distances[(b, a)] = self.distances[(a, b)]

    def _room_pos(self, pos: int) -> tuple[int, int]:
        """Return the (row, column) tuple of a room, given it's index in a burrow string representation."""
        if pos < 11:
            # in hallway
            return (0, pos)
        else:
            row = ((pos - 11) // 4) + 1
            col = (((pos - 11) % 4) + 1) * 2
            return (row, col)

    def _path_length(self, pos_from: int, pos_to: int) -> int:
        """Calculate the number of steps required to get from pos_from to pos_to."""
        f = self.positions[pos_from]
        t = self.positions[pos_to]

        # if not in the same room, the number of steps is:
        #   row[f] + number of hallway steps between f and t + row[t]
        # if in the same room, the number of steps is:
        #   abs(row[f] - row[t])
        if f[1] != t[1]:
            return f[0] + abs(f[1] - t[1]) + t[0]
        else:
            return abs(f[0] - t[0])

    def path_cost(self, steps: int, p_type: str) -> int:
        """Return the cost of moving a pod of the provided type by the number of steps."""
        return steps * self.COST[p_type]

    def movers(self, burrow: str) -> list[int]:
        """Analyze a burrow string representation and generate a list of pods (identified by their
        position in the string) who can move."""
        # find all characters and their positions
        positions = [(str_pos, char)
                     for str_pos, char in enumerate(burrow) if char in 'ABCD']

        results = []
        for str_pos, char in positions:
            pos = self.positions[str_pos]
            match pos:
                case (0, _):
                    # check if in a hallway - assume it can move
                    results.append(str_pos)
                case (r, c):
                    # if not in the hallway: if pod is in the wrong room, it will have to move in any case
                    # path_from_room_free can then check if it can exit the room.
                    target_room = self.ROOMS[char]
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

    def target_room_free(self, burrow: str, pod_type: str) -> tuple[bool, int]:
        """Return if the target room for a given pod type is free to move into, and if yes, 
        which position can be moved into (deepest row that is free). 

        Returns a tuple of (bool, int) = (True if room can be moved into, position that can be moved to).
        """
        target_room = self.ROOMS[pod_type]
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

    def path_from_room_free(self, burrow: str, pos_from: int) -> bool:
        """Return if the pod at given position can exit the room it is in."""
        # if the pod is in the hallway, the room is free by default
        if pos_from < 11:
            return True
        # check which row the pod is in
        row, _ = self.positions[pos_from]
        # check that all rows above are free
        if all(burrow[x] == '.' for x in (pos_from - i * 4 for i in range(1, row))):
            return True

        return False

    def hallway_free(self, burrow: str, pos_from: int, pos_to: int) -> bool:
        """Return if the hallway between two positions is free."""
        # get hallway position if pos_from is in a room
        col_from = self.positions[pos_from][1]
        col_to = self.positions[pos_to][1]
        if col_from < col_to:
            f = col_from + 1
            t = col_to
        else:
            f = col_to + 1
            t = col_from
        hallway = burrow[f:t]
        return hallway == '.' * (t - f)

    def possible_moves(self, burrow: str, pos_from: int) -> list[tuple[int, int]]:
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
        target_free, target_pos = self.target_room_free(burrow, p_type)
        if target_free and self.hallway_free(burrow, pos_from, target_pos) and self.path_from_room_free(burrow, pos_from):
            locations_to.append(target_pos)
        else:
            # Otherwise, the pod can move to a hallway position if it is in a room and can move out of the room
            if pos_from > 10 and self.path_from_room_free(burrow, pos_from):
                for loc in [0, 1, 3, 5, 7, 9, 10]:
                    if (burrow[loc] == '.' and
                            self.hallway_free(burrow, pos_from, loc)):
                        locations_to.append(loc)

        # calculate the cost for each step
        results = []
        for pos_to in locations_to:
            steps = self.distances[(pos_from, pos_to)]
            cost = self.path_cost(steps, p_type)
            results.append((cost, pos_to))

        return results

    def move_to(self, burrow: str, pos_from: int, pos_to: int) -> str:
        """Perform a move of a pod from / to and return the new state of the burrow as a string."""
        b = list(burrow)
        b[pos_to], b[pos_from] = b[pos_from], b[pos_to]
        return ''.join(b)

    def heuristic(self, burrow: str) -> int:
        """Returns the sum of horizontal move cost for all pods not in the correct room."""
        # find all characters and their positions
        positions = [(str_pos, char)
                     for str_pos, char in enumerate(burrow) if char in 'ABCD']

        result = 0
        for str_pos, char in positions:
            # get column position for pod and the target room for the pod
            # using the first entry of the rooms for pod type
            _, col_from = self.positions[str_pos]
            _, col_to = self.positions[self.ROOMS[char][0]]
            result += self.COST[char] * abs(col_from - col_to)

        return result

    def astar(self, start: str, target: str) -> int:
        """Run a Dijkstra search for the cheapest path from start to target.

        Return the cost of the path.
        """

        # queue = state of the burrow (which includes the cost)
        q = [(0, start)]
        cost_so_far = {start: 0}
        paths = defaultdict(list)
        steps = 0
        while q:
            _, cur_state = heappop(q)
            steps += 1
            # logging.debug(
            #     f'Dijkstra: {steps=} {cost_so_far[cur_state]=} {cur_state=}')

            # if already seen, discard

            # if we found the target, we're done
            if cur_state == target:
                print(
                    f'Target reached: {cur_state}, cost {cost_so_far[cur_state]}.')
                print(f'Target path: {paths[target]}')
                print(f'Number of states processed: {steps=}')
                # logging.info(
                #     f'Target reached: {cur_state}, cost {cur_cost}.')
                # logging.info(f'Target path: {paths[target]}')
                # logging.info(f'Number of states processed: {steps=}')
                return cost_so_far[cur_state]

            # get a list of all possible movers...
            for p in self.movers(cur_state):
                # ...and their possible moves
                for inc_cost, move_loc in self.possible_moves(cur_state, p):
                    next_move = self.move_to(cur_state, p, move_loc)
                    next_cost = cost_so_far[cur_state] + inc_cost
                    if next_move not in cost_so_far or next_cost < cost_so_far[next_move]:
                        cost_so_far[next_move] = next_cost
                        paths[next_move] = paths[cur_state] + [next_move]
                        prio = next_cost + self.heuristic(next_move)
                        heappush(q, (prio, next_move))

        # logging.info(f'Target path: {paths[target]}')
        return cost_so_far[target]


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        lines = f.readlines()
        for line in lines[2:-1]:
            pods = list(line.strip().replace('#', ''))
            puzzle_input.extend(pods)

    return puzzle_input


def to_string(puzzle_input: list[str]) -> str:
    """Convert the puzzle input list (a list of 8 characters, representing the 4 rooms of the
    puzzle) into a string with the format '............ABCDABCD', representing the hallway
    and 4 rooms.
    """
    return '.' * 11 + ''.join(puzzle_input)


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    start = to_string(puzzle_input)
    target = to_string(list(['ABCD' * 2]))
    # target = to_string(['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'])

    # # run the dijkstra search to find the shortest path
    solver = Solver(2)
    cost = solver.astar(start, target)

    return cost


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    start = to_string(puzzle_input)
    target = to_string(list(['ABCD' * 4]))

    # # run the dijkstra search to find the shortest path
    solver = Solver(4)
    cost = solver.astar(start, target)

    return cost


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, filename="23_reduced_steps.log")

    # read the puzzle input
    puzzle_input = load_input('input/23.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    puzzle_input = load_input('input/23_2.txt')
    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 14:15 End: 18:45 (16 January - solution was working a long time ago, but now optimized)
# Part 2: Start: 19:03 End: 19:10
