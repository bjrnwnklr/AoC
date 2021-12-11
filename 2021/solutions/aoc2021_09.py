# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(list(map(int, list(line.strip()))))

    return puzzle_input


class Grid:
    def __init__(self, g) -> None:
        self.floormap = {
            (r, c): n
            for r, row in enumerate(g)
            for c, n in enumerate(g[r])
        }
        self.lp = self.low_points()

    def neighbors(self, r, c):
        neighbors = []
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in self.floormap:
                neighbors.append((nr, nc))

        return neighbors

    def is_low_point(self, r, c):
        height = self.floormap[(r, c)]
        return all(
            height < self.floormap[(nr, nc)]
            for nr, nc in self.neighbors(r, c)
        )

    def low_points(self):
        return [
            (r, c)
            for r, c in self.floormap
            if self.is_low_point(r, c)
        ]

    def risk_level(self, r, c):
        return self.floormap[(r, c)] + 1

    def sum_of_risk_levels(self):
        return sum(self.risk_level(r, c) for r, c in self.lp)

    # Part 2 methods
    def size_of_basin(self, r, c):
        """Returns the size of a basin around a low point (the input parameter)."""
        # this is a flood fill with 9s and the grid as the boundaries
        q = [(r, c)]
        filled = set()
        while q:
            cp = q.pop(0)
            if cp not in filled:
                filled.add(cp)
                for np in self.neighbors(*cp):
                    if self.floormap[np] < 9:
                        q.append(np)

        return len(filled)

    def three_basins_size(self):
        basins = [
            self.size_of_basin(r, c)
            for r, c in self.lp
        ]

        result = 1
        for b in sorted(basins, reverse=True)[:3]:
            result *= b

        return result


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    grid = Grid(puzzle_input)

    return grid.sum_of_risk_levels()


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    grid = Grid(puzzle_input)

    return grid.three_basins_size()


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/09.txt')
    # puzzle_input = load_input('testinput/09_1_1.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 17:01 End: 17:26
# Part 2: Start: 17:27 End: 17:43

"""
Elapsed time to run part1: 0.01892 seconds.
Part 1: 465
Elapsed time to run part2: 0.03059 seconds.
Part 2: 1269555
"""
