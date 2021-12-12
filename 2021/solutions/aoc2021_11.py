# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer


class Grid:
    def __init__(self, inp) -> None:
        self.pl = {
            (r, c): int(n)
            for r, line in enumerate(inp)
            for c, n in enumerate(line)
        }
        self.flashes = 0
        self.already_flashed = set()
        self.all_octopi = len(self.pl)
        self.all_flashed = False

    def neighbors(self, r, c):
        neigh = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in self.pl and (dr, dc) != (0, 0):
                    neigh.append((nr, nc))

        return neigh

    def cycle(self):
        flashed = True
        self.all_flashed = False
        # increase energy level by 1 for all octopi
        for r, c in self.pl:
            self.pl[(r, c)] += 1

        while flashed:
            flashed = False
            # collect all octopi that have not yet flashed with > 9
            next_flash = [
                (r, c) for r, c in self.pl
                if self.pl[(r, c)] > 9 and
                (r, c) not in self.already_flashed
            ]
            for r, c in next_flash:
                flashed = True
                self.flashes += 1
                self.already_flashed.add((r, c))
                # increase all neighbors
                for nr, nc in self.neighbors(r, c):
                    self.pl[(nr, nc)] += 1

        # reset all flashed octopi to 0
        for r, c in self.already_flashed:
            self.pl[(r, c)] = 0

        # part 2: check if all octopi have flashed in this step
        if len(self.already_flashed) == self.all_octopi:
            self.all_flashed = True

        self.already_flashed = set()


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    g = Grid(puzzle_input)
    for _ in range(100):
        g.cycle()

    return g.flashes


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    g = Grid(puzzle_input)
    i = 1
    while True:
        g.cycle()
        if g.all_flashed:
            # all octopi have flashed, return the number
            return i
        i += 1


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/11.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 15:13 End: 15:45
# Part 2: Start: 15:53 End: 15:57
