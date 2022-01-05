# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer

COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}


class Burrow:
    """Defines a state of the burrow at any given time.
    State is defined by the location of each amphipod.
    """
    target_room = {
        'A': 2,
        'B': 4,
        'C': 6,
        'D': 8
    }

    def __init__(self, pod_locations: list[str]) -> None:
        """Load the amphipod's locations from the list provided:

        The list contains the 8 amphipods in from left to right in the first row, 
        then again from left to right in the second row.

        The burrow has the following layout:

        row 0: 11 cols:     (0, 0) - (0, 10)
        row 1: 4 cols:      (1, 2), (1, 4), (1, 6), (1, 8)
        row 2: 4 cols:      (2, 2), (2, 4), (2, 6), (2, 8)
        """
        self.grid = {
            (0, c): '.'
            for c in range(11)
        }
        # dictionary pod_id: position (id is assigned sequentially per initial state)
        self.pods = {}
        for i, pod in enumerate(pod_locations):
            r = 1 if i < 4 else 2
            c = ((2 * i) % 8 + 2)
            self.grid[(r, c)] = pod
            self.pods[i] = (r, c)

    def state(self) -> str:
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
        result = ''.join(self.grid[(0, c)] for c in range(11))
        result += ''.join(self.grid[(1, c)] for c in range(2, 9, 2))
        result += ''.join(self.grid[(2, c)] for c in range(2, 9, 2))
        return result

    def can_move(self) -> list[tuple[str, tuple[int]]]:
        """Return all pods that can (theoretically) move:

        - They are in the upper row of a room
        - They are in the lower row of a room with no pod above
        - They are in a hallway location (they can only move if they have a path to the correct room)
        """
        movers = []
        for id in self.pods:
            match self.pods[id]:
                case (1, _):
                    movers.append(id)
                case (2, c):
                    if self.grid[(1, c)] == '.':
                        movers.append(id)
                case (0, c):
                    # If a pod is in the hallway, check if a slot in the target room is available
                    # and if another pod is in there, if it is of the same kind. Then check if the path
                    # to the target room is free.
                    pod_type = self.pods[id]
                    target_col = self.target_room[pod_type]
                    # First, check if the target room is free
                    if ((self.grid[(1, target_col)] == '.' and self.grid[(2, target_col)] == '.') or
                            (self.grid[(1, target_col)] == '.' and self.grid[(2, target_col)] == pod_type)):
                        # calculate if the path to the target room is free
                        if c < target_col:
                            target_path = all(
                                self.grid[(0, x)] == '.' for x in range(c + 1, target_col + 1))
                        else:
                            target_path = all(
                                self.grid[(0, x)] == '.' for x in range(target_col, c))

                        # Pod can only move if target room is free and the path is free.
                        if target_path:
                            movers.append(id)

        return movers

    def __eq__(self, __o: 'Burrow') -> bool:
        return self.state() == __o.state()

    def __repr__(self) -> str:
        result = '#############\n'

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


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    # TODO: Consider if states are equal (since A and A are the same)

    b = Burrow(puzzle_input)
    print()
    print('Initial state.')
    print(b)
    print(b.state())
    target = Burrow(['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'])
    print()
    print('Target state:')
    print(target)
    print(target.state())

    # check who can move
    print('Checking who can move in initial state.')
    print(b.can_move())

    return 1


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
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
