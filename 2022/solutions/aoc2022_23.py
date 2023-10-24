# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    elves = set()
    with open(f_name, "r") as f:
        for row, line in enumerate(f.readlines()):
            for col, c in enumerate(list(line.strip())):
                if c == "#":
                    elves.add((row, col))

    return elves


class NeighborPositions:
    def __init__(self):
        self.total = 0
        # count of elves seen when looking
        # north, south, west, east
        self.dirs = [0, 0, 0, 0]


def evaluate(elf, elves):
    """Evaluate an elf's position and return
    a NeighborPositions object."""
    np = NeighborPositions()
    for dr, dc in [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]:
        if (elf[0] + dr, elf[1] + dc) in elves:
            np.total += 1
            # north
            if dr == -1:
                np.dirs[0] += 1
            # south
            if dr == 1:
                np.dirs[1] += 1
            # west
            if dc == -1:
                np.dirs[2] += 1
            # east
            if dc == 1:
                np.dirs[3] += 1

    return np


# north, south, west, east
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def rect_dims(elves):
    """Return the edges of the rectangle formed by
    the elves."""
    min_r = min(r for r, c in elves)
    max_r = max(r for r, c in elves)
    min_c = min(c for r, c in elves)
    max_c = max(c for r, c in elves)

    return min_r, max_r, min_c, max_c


def print_rect(elves):
    """Print a representation of the rectangle containing the elves."""
    min_r, max_r, min_c, max_c = rect_dims(elves)
    for r in range(min_r, max_r + 1):
        line = "".join("#" if (r, c) in elves else "." for c in range(min_c, max_c + 1))
        print(line)


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # step 1 - evaluate if elves can move
    # if an elf can move, add their new position
    # - to a dictionary old_pos: new_pos so it can be
    #   iterated over in step 2
    # - to a defaultdict(int) to count how many times the
    #   new position is taken
    #   in step 2, we check if the position has been taken
    #   multiple times

    elves = puzzle_input.copy()

    # indicates where the moves start in this round
    # 0: north, 1: south, 2: west, 3: east
    move_start = 0

    # loop for 10 times
    for round in range(10):
        next_positions = dict()
        pos_count = defaultdict(int)

        for elf in elves:
            # get neighbors of each elf
            np = evaluate(elf, elves)
            if np.total == 0 or all(np.dirs):
                # no other elves in any direction, or elves in all directions
                # Elf stays where they are
                next_positions[(elf)] = elf
                pos_count[elf] += 1
                # don't add to pos_count as we assume nobody is going
                # to move to a position where there is already an elf
                continue
            for i in range(4):
                look_dir = (move_start + i) % 4
                if np.dirs[look_dir] == 0:
                    # move to that direction and stop looking
                    rr = elf[0] + moves[look_dir][0]
                    cc = elf[1] + moves[look_dir][1]
                    # register the move for next step
                    next_positions[(elf)] = (rr, cc)
                    # count how many moves would go to the same position
                    pos_count[(rr, cc)] += 1
                    # stop looking
                    break

        # step 2, evaluate and execute moves
        new_board = set()
        for elf in elves:
            assert elf in next_positions
            assert next_positions[elf] in pos_count
            if pos_count[next_positions[elf]] > 1:
                # do not move
                new_board.add(elf)
            else:
                # add new position to board
                new_board.add(next_positions[elf])

        # done with moves, prepare for next round
        elves = new_board.copy()
        # increase move_start
        move_start += 1

    # done with rounds, count how many empty ground tiles
    # are in the smallest rectangle around the elves
    # find smallest / largest coordinates of the elves
    # count how many elves are in the rectangle
    min_r, max_r, min_c, max_c = rect_dims(elves)
    e_in_r = [x for x in elves if min_r <= x[0] <= max_r and min_c <= x[1] <= max_c]
    # dimensions of the rectangle
    rect_area = (max_r - min_r + 1) * (max_c - min_c + 1)
    # result is the area of the rectangle - number of elves in the rectangle
    result = rect_area - len(e_in_r)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    elves = puzzle_input.copy()

    # indicates where the moves start in this round
    # 0: north, 1: south, 2: west, 3: east
    move_start = 0

    # loop until no elf moves
    for round in range(100_000):
        moved = False
        next_positions = dict()
        pos_count = defaultdict(int)

        for elf in elves:
            # get neighbors of each elf
            np = evaluate(elf, elves)
            if np.total == 0 or all(np.dirs):
                # no other elves in any direction, or elves in all directions
                # Elf stays where they are
                next_positions[(elf)] = elf
                pos_count[elf] += 1
                # don't add to pos_count as we assume nobody is going
                # to move to a position where there is already an elf
                continue
            for i in range(4):
                look_dir = (move_start + i) % 4
                if np.dirs[look_dir] == 0:
                    # move to that direction and stop looking
                    rr = elf[0] + moves[look_dir][0]
                    cc = elf[1] + moves[look_dir][1]
                    # register the move for next step
                    next_positions[(elf)] = (rr, cc)
                    # count how many moves would go to the same position
                    pos_count[(rr, cc)] += 1
                    # stop looking
                    moved = True
                    break

        # part 2: break if nobody moved
        if not moved:
            break

        # step 2, evaluate and execute moves
        new_board = set()
        for elf in elves:
            assert elf in next_positions
            assert next_positions[elf] in pos_count
            if pos_count[next_positions[elf]] > 1:
                # do not move
                new_board.add(elf)
            else:
                # add new position to board
                new_board.add(next_positions[elf])

        # done with moves, prepare for next round
        elves = new_board.copy()
        # increase move_start
        move_start += 1

    return round + 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/23.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 17:00 End: 18:40
# Part 2: Start: 18:40 End: 18:51

# Elapsed time to run part1: 0.04718 seconds.
# Part 1: 4049
# Elapsed time to run part2: 4.12996 seconds.
# Part 2: 1021
