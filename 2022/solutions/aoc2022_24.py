# Load any required modules. Most commonly used:

from dataclasses import dataclass

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    # Extract ints from the input
    #
    # signed ints
    # regex = re.compile(r"(-?\d+)")
    #
    # unsigned ints
    # regex = re.compile(r"(\d+)")
    #
    # with open(f_name, "r") as f:
    #     puzzle_input = []
    #     for line in f.readlines():
    #         matches = regex.findall(line.strip())
    #         if matches:
    #             puzzle_input.append(list(map(int, matches)))

    return puzzle_input


# directions of the blizzards and movements (so including a 'wait' state)
directions = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0), "w": (0, 0)}


@dataclass
class Blizzard:
    r: int
    c: int
    d: str


def generate_map(puzzle_input):
    """Generate two outputs from the puzzle_input:
    - walls: a tuple of coordinates for the bottom right
             corner e.g. (8, 10). Walls are then in
             row 0 and 8, and columns 0 and 10.

    - blizzards: a list of blizzards, which are
                 instances of the blizzard dataclass
                 with r, c, dir.
    """
    walls = (len(puzzle_input) - 1, len(puzzle_input[0]) - 1)
    blizzards = []
    for r, row in enumerate(puzzle_input):
        for c, col in enumerate(row):
            if col in directions:
                blizzards.append(Blizzard(r, c, col))
    return walls, blizzards


def move_blizzards(walls, blizzards):
    """Generate the next state of the blizzards by moving forward
    by one minute. Returns a new list of blizzard objects and a set
    of blizzard coordinates.

    Assumption is that no blizzard moves to the start or end position!
    """
    next_state = []
    b_coords = set()
    for b in blizzards:
        # add direction
        new_row = b.r + directions[b.d][0]
        new_col = b.c + directions[b.d][1]
        # check if any wall was hit
        # a modulo calculation
        new_row = ((new_row - 1) % (walls[0] - 1)) + 1
        new_col = ((new_col - 1) % (walls[1] - 1)) + 1
        next_state.append(Blizzard(new_row, new_col, b.d))
        b_coords.add((new_row, new_col))

    return next_state, b_coords


def draw_state(walls, blizzards):
    """Draw the current state."""
    # calculate blizzard coordinates
    b_coords = dict()
    for b in blizzards:
        if (b.r, b.c) in b_coords:
            b_coords[(b.r, b.c)] = (
                b_coords[(b.r, b.c)][1] + 1,
                b_coords[(b.r, b.c)][1] + 1,
            )
        else:
            b_coords[(b.r, b.c)] = (b.d, 1)

    print("#." + "#" * (walls[1] - 1))
    for r in range(1, walls[0]):
        s = "#"
        for c in range(1, walls[1]):
            if (r, c) in b_coords:
                s += str(b_coords[(r, c)][0])
            else:
                s += "."
        s += "#"
        print(s)
    print("#" * (walls[1] - 1) + ".#")


def BFS(start, end, blizzards, walls):

    # run a BFS:
    # - each minute is a state. Minutes have the same configuration of blizzards
    # - state stores: (current pos, minute)
    # - we have a dictionary with minutes which retrieve the map of blizzards for
    #   the respective minute so it doesnt have to be generated again
    state = (start, 0)
    # calculate initial blizzard coordinates from blizzards
    b_coords = set((b.r, b.c) for b in blizzards)
    blizzard_state = {0: (blizzards[:], b_coords)}
    seen = set()
    q = [state]
    while q:
        curr_pos, minute = q.pop(0)
        # print(f"Next item from queue: {curr_pos}, minute {minute}")
        if (curr_pos, minute) in seen:
            continue
        seen.add((curr_pos, minute))

        # check if we have reached the end
        if curr_pos == end:
            break

        # add next states:
        # - move in any direction
        # - wait (there is probably some optimization here - wait only if no
        #   possible next step?)
        next_minute = minute + 1
        # check if blizzard state for this minute has been generated before
        if next_minute not in blizzard_state:
            # generate new state
            blizzard_state[next_minute] = move_blizzards(
                walls, blizzard_state[next_minute - 1][0]
            )
        next_state, b_coords = blizzard_state[next_minute]
        for d in directions.values():
            rr = curr_pos[0] + d[0]
            cc = curr_pos[1] + d[1]
            if (
                (rr, cc) == end
                or (rr, cc) == start
                or (
                    0 < rr < walls[0] and 0 < cc < walls[1] and (rr, cc) not in b_coords
                )
            ):
                q.append(((rr, cc), next_minute))

    # return the earliest minute and the state of the blizzards during that minute
    return minute, blizzard_state[minute][0]


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # generate the map - top left corner is (0, 0) (r, c)
    # start point - (0, 1)
    # end point - bottom right -1
    # walls
    # blizzards
    walls, blizzards = generate_map(puzzle_input)
    start = (0, 1)
    end = (walls[0], walls[1] - 1)

    minute, blizzards = BFS(start, end, blizzards, walls)
    # for minute in range(19):
    #     print(f"Minute {minute}")
    #     draw_state(walls, blizzards)
    #     blizzards = move_blizzards(walls, blizzards)
    #     print()

    return minute


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    result = 0
    walls, blizzards = generate_map(puzzle_input)
    start = (0, 1)
    end = (walls[0], walls[1] - 1)

    # first pass, from start to end
    minute, blizzards = BFS(start, end, blizzards, walls)
    result += minute

    # second pass, from end to start
    minute, blizzards = BFS(end, start, blizzards, walls)
    result += minute

    # third pass, from start to end
    minute, blizzards = BFS(start, end, blizzards, walls)
    result += minute

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/24.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 14:09 End: 15:59
# Part 2: Start: 16:00 End: 16:12

# Elapsed time to run part1: 0.86204 seconds.
# Part 1: 221
# Elapsed time to run part2: 3.19891 seconds.
# Part 2: 739
