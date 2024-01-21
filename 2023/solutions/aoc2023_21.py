# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
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

    return puzzle_input


def parse_grid(puzzle_input):
    """Parse the input into:
    - set of rocks
    - starting position
    - boundaries (width / height)"""
    rocks = set()
    width = len(puzzle_input[0])
    height = len(puzzle_input)
    for r, row in enumerate(puzzle_input):
        for c, cell in enumerate(row):
            if cell == "#":
                rocks.add((r, c))
            elif cell == "S":
                start = (r, c)

    return rocks, start, width, height


def BFS(rocks, start, width, height, steps, even=True):
    """Run a BFS on the grid to find the number of possible positions
    that can be reached within given number of steps.

    This could also mean that we just step back and forth multiple times."""
    seen = set()
    # dictionary: number of steps: [positions reached]
    reached_by_steps = defaultdict(set)
    # position, number of steps taken
    q = [(start, 0)]
    while q:
        curr_pos, curr_steps = q.pop(0)

        if curr_pos in seen:
            continue

        seen.add(curr_pos)
        reached_by_steps[curr_steps].add(curr_pos)

        # generate next steps
        for dr, dc in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
            next_pos = (curr_pos[0] + dr, curr_pos[1] + dc)
            if (
                0 <= next_pos[0] < height
                and 0 <= next_pos[1] < width
                and next_pos not in rocks
                and curr_steps + 1 <= steps
            ):
                q.append((next_pos, curr_steps + 1))

    # when we get here, we have evaluated all possible steps to reach each cell
    # while not going over the number of required steps
    # return the number of positions that can be reached in number of steps
    # this is determined by all possible positions that can be reached in an
    # even number of steps - as we can just step back and forth, so reach
    # the same position in 2, 4, 6, 8 etc steps
    step_remainder = 0 if even else 1
    all_positions = set()
    for x in reached_by_steps:
        if x % 2 == step_remainder:
            all_positions |= reached_by_steps[x]

    return len(all_positions)


@aoc_timer
def part1(puzzle_input, steps):
    """Solve part 1. Return the required output value."""
    rocks, start, width, height = parse_grid(puzzle_input)
    result = BFS(rocks, start, width, height, steps)

    return result


@aoc_timer
def part2(puzzle_input, steps):
    """Solve part 2. Return the required output value."""

    # calculate some basic parameters
    # width / height are the same, required to calculate the
    # number of tiles etc
    rocks, start, width, height = parse_grid(puzzle_input)
    # number of tiles
    n = steps // width
    # distance from middle to edges
    s = steps % width

    # Based on the number of tiles, the diamond formed by the tiles is made up of
    # Even tiles (E), Odd tiles (O), Corners (C), Type A edge (A), Type B edge (B)
    # The diamond has this number of tiles:
    # (n-1)**2 * O + n**2 * E + C + (n-1) * A + n * B
    # Calculate the number of cells reachable for each type of tile and the available steps

    # Even:
    # - start in the middle,
    # - infinite steps (width + s = 131 + 65 is sufficient to reach every cell)
    # - even steps only
    E = BFS(rocks, (s, s), width, height, width + s, even=True)
    # Odd:
    # - start in the middle,
    # - infinite steps
    # - odd steps only
    O = BFS(rocks, (s, s), width, height, width + s, even=False)
    # Corners
    # - start in the middle of each outer edge,
    # - width steps = 130 (even)
    #   Only 130 steps left from here as we use the first step
    #   to step into the last tile, so this tile is funnily enough even!
    # - even steps only
    steps_c = width - 1
    even_steps = True
    C1 = BFS(rocks, (width - 1, s), width, height, steps_c, even_steps)
    C2 = BFS(rocks, (s, 0), width, height, steps_c, even_steps)
    C3 = BFS(rocks, (0, s), width, height, steps_c, even_steps)
    C4 = BFS(rocks, (s, width - 1), width, height, steps_c, even_steps)
    # Type A edge tiles
    # - start in the corner of each outer edge,
    # - width + s - 1 steps = 131 + 65 - 1 = 195 (odd)
    # - odd steps only
    steps_a = width + s - 1
    even_steps = False
    A1 = BFS(rocks, (width - 1, 0), width, height, steps_a, even_steps)
    A2 = BFS(rocks, (0, 0), width, height, steps_a, even_steps)
    A3 = BFS(rocks, (0, width - 1), width, height, steps_a, even_steps)
    A4 = BFS(rocks, (width - 1, width - 1), width, height, steps_a, even_steps)
    # Type B edge tiles
    # - start in the corner of each outer edge,
    # - s - 1 steps = 65 - 1 = 64 (even)
    #      (-1 since we have to spend one step to step into the last tile)
    # - even steps only
    steps_b = s - 1
    even_steps = True
    B1 = BFS(rocks, (width - 1, 0), width, height, steps_b, even_steps)
    B2 = BFS(rocks, (0, 0), width, height, steps_b, even_steps)
    B3 = BFS(rocks, (0, width - 1), width, height, steps_b, even_steps)
    B4 = BFS(rocks, (width - 1, width - 1), width, height, steps_b, even_steps)

    # add everything up
    C = C1 + C2 + C3 + C4
    A = A1 + A2 + A3 + A4
    B = B1 + B2 + B3 + B4
    result = (n - 1) ** 2 * O + n**2 * E + C + (n - 1) * A + n * B
    print(f"Odd: {O}")
    print(f"Even: {E}")
    print(f"Corners: {C}")
    print(f"\tC1: {C1}")
    print(f"\tC2: {C2}")
    print(f"\tC3: {C3}")
    print(f"\tC4: {C4}")
    print(f"A type: {A}")
    print(f"B type: {B}")

    # Correct answer: 627960775905777

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/21.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input, 64)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input, 26501365)
    print(f"Part 2: {p2}")

# Part 1: Start: 10:54 End: 11:31
# Part 2: Start: 11:32 End: 14:33

# Elapsed time to run part1: 0.01290 seconds.
# Part 1: 3768
# Odd: 7656
# Even: 7688
# Corners: 23066
#         C1: 5758
#         C2: 5766
#         C3: 5775
#         C4: 5767
# A type: 26845
# B type: 3920
# Elapsed time to run part2: 0.18354 seconds.
# Part 2: 627960775905777
