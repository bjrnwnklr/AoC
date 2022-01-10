# Load any required modules. Most commonly used:

# import re
import logging
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
import copy

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


@dataclass
class Pod:
    pid: int
    type: str
    pos: tuple[int]
    locked: bool = False


class Burrow:
    """Defines a state of the burrow at any given time.
    State is defined by the location of each amphipod.
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
        # dictionary pod_id: position (id is assigned sequentially per initial state)
        self.pods = {}          # pid: position
        self.cost = 0           # cost to achieve current state from start state

        # add pod locations to grid etc
        for i, pod in enumerate(pod_locations):
            # calculate which room (row, column) each pod is initially in
            r = (i // 4) + 1  # 1 if i < 4 else 2
            c = ((2 * i) % 8 + 2)
            # pods are numbered sequentially
            self.pods[i] = Pod(i, pod, (r, c))

        # pids that are locked in position because they are in the correct room
        for p in self.pods.values():
            self.lock(p)

    def lock(self, p: Pod) -> None:
        """Check if given pod should be locked in:
        - if they are on row 2 and in the correct room
        - if they are on row 1 and the pod in row 2 is also correct

        If yes, add to self.locked.
        """
        # check if in the correct column and not locked already
        if not p.locked and TARGET_ROOM[p.type] == p.pos[1]:
            match p.pos:
                case (2, _):
                    p.locked = True
                case (1, c):
                    # check if there is any other pod further down and of the same (correct) type
                    for op in self.pods.values():
                        if (op.pos[1] == c and          # same column
                                    op != p and             # not the same pod
                                    # in a row further down
                                    op.pos[0] > p.pos[0] and
                                    op.type == p.type       # same type as p
                                ):
                            p.locked = True

    def state(self) -> tuple[int, str]:
        """Returns a string representation of the current state, which 
        can be used to compare to other burrow states.

        State is represented by strings with the following format:
        - 11 characters, representing the hallway
        - 4 characters, representing the upper layer of rooms
        - 4 characters, representing the lower layer of rooms
        Each character is either ['A', 'B', 'C', 'D'] or '.' for empty spaces.

        Example:
        '...........ABCDABCD' - target state
        """
        result = [
            '.'] * 19  # create a 11 + 4 + 4 list of dots, then add individual locations
        for p in self.pods.values():
            match p.pos:
                case (0, c):
                    result[c] = p.type
                case (r, c):
                    str_pos = 10 + (r - 1) * 4 + c // 2
                    result[str_pos] = p.type
        return ''.join(result)

    def moving_cost(self, p: Pod, target_loc: tuple[int]) -> int:
        """Determine move cost from the pod to the specified location. Returns 0 if path is not free."""
        steps = 0
        cost_factor = COST[p.type]
        other_pod_locations = {op.pos for op in self.pods.values() if op != p}
        # first check if the actual target location is not occupied!
        if target_loc in other_pod_locations:
            return 0
        # check hallway by looking at each column location
        # sort the columns of the pod and target location so we can build a range for each location to check
        sorted_locations = sorted([p.pos, target_loc], key=lambda x: x[1])
        hallway_path = range(
            sorted_locations[0][1], sorted_locations[1][1] + 1)
        # if any other pod in between pod and target location, stop and return 0
        if any((0, c) in other_pod_locations for c in hallway_path):
            return 0
        else:
            steps += sorted_locations[1][1] - sorted_locations[0][1]
        # check room where pod is (if it is in a room)
        match p.pos:
            case (1, _):
                steps += 1
            case (r, c) if r > 1:
                if any((nr, c) in other_pod_locations for nr in range(1, r)):
                    return 0
                else:
                    steps += r
        # check room where pod goes to (if it goes to a room)
        match target_loc:
            case (1, _):
                steps += 1
            case (r, c) if r > 1:
                if any((nr, c) in other_pod_locations for nr in range(1, r)):
                    return 0
                else:
                    steps += r

        # if we get to here, the path is free
        # multiply number of steps with the move cost factor for the pod type to get the cost
        return steps * cost_factor

    def possible_moves(self) -> list[tuple[Pod, int, tuple[int]]]:
        """Return a list of possible moves as tuples (pod, cost, target location,) for all pods.

        Moves are possible for a pod if:
        - They are in the upper row of a room
        - They are in the lower row of a room with no pod above
        - They are in a hallway location and the correct room is free or only occupied by another pod
          of the same type
        """
        moves = []
        for p in self.pods.values():
            # first, check if the pod is already in the right position
            # if it is, it is skipped from further moves
            if p.locked:
                continue

            # NEW CODE STARTS HERE

            # Determine what the preferred target location (room) is
            target_col = TARGET_ROOM[p.type]
            target_pos = None
            # check occupied slots in the target room
            occupied_slots = [
                op for op in self.pods.values() if op.pos[1] == target_col and op != p]

            match len(occupied_slots):
                case 0:
                    # room is completely empty, move to row 2
                    target_pos = (2, target_col)
                case 1:
                    # lower room is occupied, check if it is indeed the lower room and if it is
                    # a matching pod
                    op = occupied_slots[0]
                    # raise exception if pod is not in row 2 - there should never be a pod in row 1 but
                    # none in row 2.
                    if op.pos[0] != 2:
                        raise AssertionError(
                            f'Pod {op} not expected in location {op.pos}.\n{self.pods=}\n{self.state()=}\n{p=}')
                    if op.type == p.type:
                        target_pos = (1, target_col)
                case 2:
                    # room is occupied, can't move there
                    pass

            if target_pos:
                cost = self.moving_cost(p, target_pos)
                if cost != 0:
                    # path is free, add a move to the location
                    moves.append((p, cost, target_pos))

            # check any moves to hallway locations if pod is not in the hallway
            if p.pos[0] != 0:
                for c in range(0, 11):
                    if c not in [2, 4, 6, 8]:
                        cost = self.moving_cost(p, (0, c))
                        if cost != 0:
                            moves.append((p, cost, (0, c)))

            # OLD CODE

            # # check which hallway positions from current location are free
            # # If we reached the left wall (0,0), we will have to subtract 1 from left, which simulates
            # # the wall at (0, -1) as the last element checked
            # left = curr_loc[1]
            # while left > 0:
            #     left -= 1
            #     if self.grid[(0, left)] == '.':
            #         continue
            #     else:
            #         left += 1
            #         break

            # left_range = range(left, curr_loc[1])

            # # If we reached the right wall (0,10), we will have to add to right, which simulates
            # # the wall at (0, 11) as the last element checked
            # right = curr_loc[1]
            # while right < 10:
            #     right += 1
            #     if self.grid[(0, right)] == '.':
            #         continue
            #     else:
            #         right -= 1
            #         break

            # right_range = range(curr_loc[1] + 1, right)

            # match curr_loc:
            #     case (1, c):
            #         # pod is in a room, move to the hallway
            #         # Don't stop in front of any rooms (2, 4, 6, 8 columns)
            #         for x in list(left_range) + list(right_range):
            #             if x not in [2, 4, 6, 8]:
            #                 # calculate the cost - add 1 for the step into the hallway
            #                 cost = (abs(c - x) + 1) * move_cost
            #                 moves.append((p, cost, (0, x)))

            #     case (2, c):
            #         if self.grid[(1, c)] == '.':
            #             # pod is in a 2nd layer room, move to the hallway
            #             # Don't stop in front of any rooms (2, 4, 6, 8 columns)
            #             for x in list(left_range) + list(right_range):
            #                 if x not in [2, 4, 6, 8]:
            #                     # calculate the cost - add 2 for the step into the hallway
            #                     cost = (abs(c - x) + 2) * move_cost
            #                     moves.append((p, cost, (0, x)))

            # # FOR ALL CASES; check if we can move directly to the correct room (from another room
            # # or hallway)
            # # Check if a slot in the target room is available and if another pod is in there,
            # # if it is of the same kind. Then check if the path to the target room is free.
            # target_col = TARGET_ROOM[pod_type]
            # # First, check if the target room is free
            # if ((self.grid[(1, target_col)] == '.' and self.grid[(2, target_col)] == '.') or
            #         (self.grid[(1, target_col)] == '.' and self.grid[(2, target_col)] == pod_type)):
            #     # calculate if the path to the target room is free
            #     c = curr_loc[1]
            #     if c < target_col:
            #         target_path = all(
            #             self.grid[(0, x)] == '.' for x in range(c + 1, target_col + 1))
            #     else:
            #         target_path = all(
            #             self.grid[(0, x)] == '.' for x in range(target_col, c))

            #     # check where we are - hallway, room 1 or room 2:
            #     match curr_loc:
            #         case (0, _):
            #             room_cost = 0
            #         case (1, _):
            #             room_cost = 1
            #         case (2, c):
            #             if self.grid[(1, c)] == '.':
            #                 room_cost = 2
            #             else:
            #                 room_cost = 0
            #                 target_path = False
            #     # Pod can only move if target room is free and the path is free.
            #     if target_path:
            #         if self.grid[(2, target_col)] == '.':
            #             room_cost += 2
            #             row = 2
            #         else:
            #             room_cost += 1
            #             row = 1
            #         cost = (abs(c - target_col) +
            #                 room_cost) * move_cost
            #         moves.append((p, cost, (row, target_col)))

        return moves

    def move_copy(self, p: Pod, inc_cost: int, target_location: tuple[int]) -> 'Burrow':
        """Move a pod to the specified target location and return a new burrow
        instance, representing the new state after the move. Add the inc_cost to the current cost.
        """
        # create an empty burrow
        # logging.debug(f'Move_copy: {p=}, {inc_cost=}, {target_location=}')
        b_copy = Burrow()
        # now copy the grid, pods and types dictionaries
        # copy is fine since the values of the dict are immutable tuples
        # FIXME: Updating the location OVERWRITES THE POD INSTANCES INSTEAD OF COPYING THEM
        # We need to deep copy or copy the pods themselves :(
        b_copy = copy.deepcopy(self)
        new_p = b_copy.pods[p.pid]
        # update the new position with the pod
        new_p.pos = target_location

        # update the cost with the incremental cost
        b_copy.cost += inc_cost

        # check if the pod is in the correct room and should be locked
        b_copy.lock(new_p)

        # return the new burrow instance
        return b_copy

    def __eq__(self, __o: 'Burrow') -> bool:
        return self.state() == __o.state()

    def __lt__(self, __o: 'Burrow') -> bool:
        # return (-len(self.locked), self.cost) < (-len(__o.locked), __o.cost)
        return self.cost < __o.cost


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
        if cur_state.state() == target.state():
            logging.info(
                f'Target reached: {cur_state.state()}, cost {cur_state.cost}.')
            logging.info(f'Target path: {paths[target.state()]}')
            return distances[target.state()]

        for p, inc_cost, move_loc in cur_state.possible_moves():
            next_move = cur_state.move_copy(p, inc_cost, move_loc)
            # DEBUG STUFF: If we're missing an element, dump the data and throw and exception.
            if next_move.state().count('.') > 11:
                raise ValueError(
                    f'Missing a pod! {next_move.state()}\n{next_move=}\n{next_move.pods=}\nLast move: {p=}, {inc_cost=}, {move_loc=}'
                )
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
    logging.basicConfig(level=logging.DEBUG)

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
