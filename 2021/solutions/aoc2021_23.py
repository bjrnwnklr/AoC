# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
from utils.aoctools import aoc_timer
from heapq import heappop, heappush
import logging

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


class Burrow:
    """Defines a state of the burrow at any given time.
    State is defined by the location of each amphipod.

    TODO: Might have to add the incurred cost to the state to avoid comparing
    cases where a different 'A' moved to the same location (crossover of cases).
    """

    def __init__(self, pod_locations: list[str] = []) -> None:
        """Load the amphipod's locations from the list provided:

        The list contains the 8 amphipods in from left to right in the first row, 
        then again from left to right in the second row.

        The burrow has the following layout:

        row 0: 11 cols:     (0, 0) - (0, 10)
        row 1: 4 cols:      (1, 2), (1, 4), (1, 6), (1, 8)
        row 2: 4 cols:      (2, 2), (2, 4), (2, 6), (2, 8)
        """
        # (r, c): A, B, C, D or .
        self.grid = {
            (0, c): '.'
            for c in range(11)
        }
        # dictionary pod_id: position (id is assigned sequentially per initial state)
        self.pods = {}          # pid: position
        self.types = {}         # pid: type (A, B, C, D)
        self.cost = 0           # cost to achieve current state from start state

        # add pod locations to grid etc
        for i, pod in enumerate(pod_locations):
            # calculate which room (row, column) each pod is initially in
            r = 1 if i < 4 else 2
            c = ((2 * i) % 8 + 2)
            self.grid[(r, c)] = pod
            self.pods[i] = (r, c)  # pods are numbered sequentially
            self.types[i] = pod

        # pids that are locked in position because they are in the correct room
        self.locked = set()
        for pid in self.pods:
            self.lock(pid)

    def lock(self, pid: int) -> None:
        """Check if given pod should be locked in:
        - if they are on row 2 and in the correct room
        - if they are on row 1 and the pod in row 2 is also correct

        If yes, add to self.locked.
        """
        # check if in the correct row
        if pid not in self.locked and TARGET_ROOM[self.types[pid]] == self.pods[pid][1]:
            match self.pods[pid]:
                case (2, _):
                    self.locked.add(pid)
                case (1, c):
                    other_pod = self.grid[(2, c)]
                    if TARGET_ROOM[other_pod] == c:
                        self.locked.add(pid)

    def state(self) -> tuple[int, str]:
        """Returns a tuple consisting of:
        - current cost to reach this state, 
        - string representation of the current state, which 
        can be used to compare to other burrow states.

        State is represented by strings with the following format:
        - 11 characters, representing the hallway
        - 4 characters, representing the upper layer of rooms
        - 4 characters, representing the lower layer of rooms
        Each character is either ['A', 'B', 'C', 'D'] or '.' for empty spaces.

        Example:
        (1800, '...........ABCDABCD') - (cost, target state)
        """
        result = ''.join(self.grid[(0, c)] for c in range(11))
        result += ''.join(self.grid[(1, c)] for c in range(2, 9, 2))
        result += ''.join(self.grid[(2, c)] for c in range(2, 9, 2))
        return (self.cost, result)

    def possible_moves(self) -> list[tuple[int, int, tuple[int]]]:
        """Return a list of possible moves as tuples (id, cost, target location,) for all pods.

        Moves are possible for a pod if:
        - They are in the upper row of a room
        - They are in the lower row of a room with no pod above
        - They are in a hallway location and the correct room is free or only occupied by another pod
          of the same type
        """
        moves = []
        for pid in self.pods:
            pod_type = self.types[pid]
            move_cost = COST[pod_type]
            curr_loc = self.pods[pid]
            # first, check if the pod is already in the right position
            # if it is, it is skipped from further moves
            if pid in self.locked:
                continue

            # check which hallway positions from current location are free
            # If we reached the left wall (0,0), we will have to subtract 1 from left, which simulates
            # the wall at (0, -1) as the last element checked
            left = curr_loc[1]
            while left > 0:
                left -= 1
                if self.grid[(0, left)] == '.':
                    continue
                else:
                    left += 1
                    break
            # left_move = 0
            # for left in range(curr_loc[1] - 1, -1, -1):
            #     if self.grid[(0, left)] != '.':
            #         left_move = left + 1
            #         break
            #     if left == 0:
            #         left_move = 0

            left_range = range(left, curr_loc[1])

            right = curr_loc[1]
            while right < 10:
                right += 1
                if self.grid[(0, right)] == '.':
                    continue
                else:
                    right -= 1
                    break
            # right_move = 11
            # for right in range(curr_loc[1] + 1, 11):
            #     if self.grid[(0, right)] != '.':
            #         right_move = right
            #         break
            #     if right == 10:
            #         right_move = 11
            # If we reached the right wall (0,10), we will have to add to right, which simulates
            # the wall at (0, 11) as the last element checked
            right_range = range(curr_loc[1] + 1, right)
            match curr_loc:
                case (1, c):
                    # pod is in a room, move to the hallway
                    # Don't stop in front of any rooms (2, 4, 6, 8 columns)
                    for x in list(left_range) + list(right_range):
                        if x not in [2, 4, 6, 8]:
                            # calculate the cost - add 1 for the step into the hallway
                            cost = (abs(c - x) + 1) * move_cost
                            moves.append((pid, cost, (0, x)))
                    # TODO: Add option to directly move to a new room (although that is covered
                    # by two consecutive moves, one into the hallway and another to the room)

                case (2, c):
                    if self.grid[(1, c)] == '.':
                        # pod is in a 2nd layer room, move to the hallway
                        # Don't stop in front of any rooms (2, 4, 6, 8 columns)
                        for x in list(left_range) + list(right_range):
                            if x not in [2, 4, 6, 8]:
                                # calculate the cost - add 2 for the step into the hallway
                                cost = (abs(c - x) + 2) * move_cost
                                moves.append((pid, cost, (0, x)))

            # FOR ALL CASES; check if we can move directly to the correct room (from another room
            # or hallway)
            # Check if a slot in the target room is available and if another pod is in there,
            # if it is of the same kind. Then check if the path to the target room is free.
            target_col = TARGET_ROOM[pod_type]
            # First, check if the target room is free
            if ((self.grid[(1, target_col)] == '.' and self.grid[(2, target_col)] == '.') or
                    (self.grid[(1, target_col)] == '.' and self.grid[(2, target_col)] == pod_type)):
                # calculate if the path to the target room is free
                c = curr_loc[1]
                if c < target_col:
                    target_path = all(
                        self.grid[(0, x)] == '.' for x in range(c + 1, target_col + 1))
                else:
                    target_path = all(
                        self.grid[(0, x)] == '.' for x in range(target_col, c))

                # check where we are - hallway, room 1 or room 2:
                match curr_loc:
                    case (0, _):
                        room_cost = 0
                    case (1, _):
                        room_cost = 1
                    case (2, c):
                        if self.grid[(1, c)] == '.':
                            room_cost = 2
                        else:
                            room_cost = 0
                            target_path = False
                # Pod can only move if target room is free and the path is free.
                if target_path:
                    if self.grid[(2, target_col)] == '.':
                        room_cost += 2
                        row = 2
                    else:
                        room_cost += 1
                        row = 1
                    cost = (abs(c - target_col) +
                            room_cost) * move_cost
                    moves.append((pid, cost, (row, target_col)))

        return moves

    def move_copy(self, pid: int, inc_cost: int, target_location: tuple[int]) -> 'Burrow':
        """Move a pod to the specified target location and return a new burrow
        instance, representing the new state after the move. Add the inc_cost to the current cost.
        """
        # create an empty burrow
        # logging.debug(f'Move_copy: {pid=}, {inc_cost=}, {target_location=}')
        b_copy = Burrow()
        # now copy the grid, pods and types dictionaries
        # copy is fine since the values of the dict are immutable tuples
        b_copy.grid = self.grid.copy()
        b_copy.pods = self.pods.copy()
        b_copy.types = self.types.copy()
        b_copy.locked = self.locked.copy()
        b_copy.cost = self.cost

        # store the old position
        old_pos = self.pods[pid]
        # update the new position with the pod
        b_copy.pods[pid] = target_location
        b_copy.grid[target_location] = self.types[pid]
        # update the old position with a '.'
        b_copy.grid[old_pos] = '.'

        # update the cost with the incremental cost
        b_copy.cost += inc_cost

        # check if the pod is in the correc room and should be locked
        b_copy.lock(pid)

        # check if any pods got lost:
        s = b_copy.state()[1]
        for x in TARGET_ROOM:
            if s.count(x) != 2:
                raise ValueError(
                    f'State is missing pods: FROM: {self.state()}, MOVE {pid}, {old_pos} {target_location} TO {b_copy.state()}, {b_copy.grid}, {b_copy.pods}')

        # return the new burrow instance
        return b_copy

    def __eq__(self, __o: 'Burrow') -> bool:
        return self.state() == __o.state()

    def __lt__(self, __o: 'Burrow') -> bool:
        return (-len(self.locked), self.cost) < (-len(__o.locked), __o.cost)
        # return self.cost < __o.cost

    def __repr__(self) -> str:
        result = f'Burrow. Cost: {self.cost}\n'

        result += '#############\n'

        result += '#'
        result += ''.join(self.grid[(0, c)] for c in range(11))
        result += '#\n'

        result += '###'
        result += '#'.join(self.grid[(1, c)] for c in range(2, 9, 2))
        result += '###\n'

        result += '  #'
        result += '#'.join(self.grid[(2, c)] for c in range(2, 9, 2))
        result += '#\n'

        result += '  #########\n'

        return result


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
    while q:
        cur_state = heappop(q)
        logging.debug(f'Dijkstra: {cur_state.state()}')

        # if already seen, discard
        if cur_state.state() in seen:
            continue

        seen.add(cur_state.state())

        # if we found the target, we're done
        if cur_state.state()[1] == target.state()[1]:
            logging.info(
                f'Target reached: {cur_state.state()}, cost {cur_state.cost}.')

        for pid, inc_cost, move_loc in cur_state.possible_moves():
            next_move = cur_state.move_copy(pid, inc_cost, move_loc)
            if next_move.state() not in seen and next_move.cost < distances[next_move.state()[1]]:
                distances[next_move.state()[1]] = next_move.cost
                paths[next_move.state()[1]] = paths[cur_state.state()
                                                    [1]] + [next_move.state()[1]]
                heappush(q, next_move)

    logging.info(f'Target path: {paths[target.state()[1]]}')
    return distances[target.state()[1]]


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    # TODO: Consider if states are equal (since A and A are the same)

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
"""
