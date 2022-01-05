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

    def __init__(self, pod_locations: list[str]) -> None:
        """Load the amphipod's locations from the list provided:

        The list contains the 8 amphipods in from left to right in the first row, 
        then again from left to right in the second row.

        The burrow has the following layout:

        row 0: 11 cols:     (0, 0) - (0, 10)
        row 1: 4 cols:      (1, 2), (1, 4), (1, 6), (1, 8)
        row 2: 4 cols:      (2, 2), (2, 4), (2, 6), (2, 8)
        """
        self.pods = set()
        self.grid = {
            (0, c): '.'
            for c in range(11)
        }
        for i, pod in enumerate(pod_locations):
            r = 1 if i < 4 else 2
            c = ((2 * i) % 8 + 2)
            self.pods.add((pod, (r, c)))
            self.grid[(r, c)] = pod

    def __eq__(self, __o: 'Burrow') -> bool:
        return self.pods == __o.pods

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

    b = Burrow(puzzle_input)
    print()
    print(b)

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
