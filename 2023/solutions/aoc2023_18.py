# Load any required modules. Most commonly used:

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

    return puzzle_input


# rows / columns, columns grow to the right, rows down
DIRS = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}


def part1_scanning(puzzle_input):
    """Solve part 1. Return the required output value."""
    pos = (0, 0)
    walls = set([pos])
    for line in puzzle_input:
        dir, steps, color = line.strip().split()
        steps = int(steps)

        # start digging in the direction and add to walls
        # ignore the color for now
        for _ in range(1, steps + 1):
            pos = (pos[0] + DIRS[dir][0], pos[1] + DIRS[dir][1])
            walls.add(pos)

    # now measure the inside of the line using scanline
    min_r = min(x[0] for x in walls)
    min_c = min(x[1] for x in walls)
    max_r = max(x[0] for x in walls)
    max_c = max(x[1] for x in walls)
    print(f"Dimensions: {min_r=}, {max_r=}, {min_c=}, {max_c=}")
    # debug: print the map
    # for r in range(min_r, max_r + 1):
    #     line = ""
    #     for c in range(min_c, max_c + 1):
    #         line += "#" if (r, c) in walls else "."
    #     print(line)
    # print("\n\n")

    volume = 0
    for r in range(min_r, max_r + 1):
        # line = ""
        # (up, down)
        previous_wall = [False, False]
        previous_cell = "."
        inside = False
        for c in range(min_c, max_c + 1):
            if (r, c) in walls:
                # Check if previous wall was going up or down
                # if change in direction of up or down, we flip inside status
                # if both had a wall in the same direction, no flip (horseshoe)
                current_wall = [False, False]
                # check neighbors up and down
                for i, (dr, dc) in enumerate([(-1, 0), (1, 0)]):
                    if (r + dr, c + dc) in walls:
                        current_wall[i] = True
                if all(current_wall):
                    # Always flip inside status if wall is going both up and down
                    inside = False if inside else True
                    previous_wall = [False, False]
                elif any(current_wall):
                    # either of the walls are going up or down, but not both
                    # only flip status if the last wall we crossed was in the other direction
                    # specifically, do not change status if the last wall was a straight line
                    if previous_cell == ".":
                        # if previous cell was no wall, we do not flip status
                        # and just update the previous wall status
                        previous_wall = current_wall[:]
                    else:
                        # previous cell was a wall, so evaluate if inside status needs to be flipped
                        # flip if the wall reversed direction from the previous
                        if not all(p == c for p, c in zip(previous_wall, current_wall)):
                            # previous wall and current wall directions are not the same, flip status
                            inside = False if inside else True
                            # store last wall status in previous_wall
                            previous_wall = [False, False]
                        else:
                            # crossed horseshoe, reset previous wall to False as not relevant
                            previous_wall = [False, False]
                else:
                    # neither wall is up or down, so we must be in the
                    # middle of a wall. Do not flip status and do not
                    # change status of previous wall
                    pass
                # walls always count as dug out volume
                volume += 1
                previous_cell = "#"
                # line += "#"
            else:
                # no wall
                # Reset previous wall status
                previous_wall = [False, False]
                previous_cell = "."
                if inside:
                    volume += 1
                    # line += "#"
                else:
                    # line += "."
                    pass
        # print(line)

    return volume


def shoelace(nodes):
    """Calculate the area contained by the coordinates given by the nodes."""
    r, c = zip(*nodes)
    area = (
        abs(
            sum(i * j for i, j in zip(r, c[1:] + c[:1]))
            - sum(i * j for i, j in zip(r[1:] + r[:1], c))
        )
        // 2
    )

    return area


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    pos = (0, 0)
    nodes = []
    outer = 0
    for line in puzzle_input:
        dir, steps, color = line.strip().split()
        steps = int(steps)
        outer += steps

        pos = (pos[0] + DIRS[dir][0] * steps, pos[1] + DIRS[dir][1] * steps)
        nodes.append(pos)

    inner = shoelace(nodes)
    # using Pick's theorem: Area = Inner + (len(outer) / 2) - 1
    # but we need to account for convex corners, as in the End
    # the form is always a derivation of a square, so will have 4 convex
    # corners more than concave
    #
    # intuitively, we have
    # - inner squares - completely included
    # - for each wall, we have half a square
    # - add 1 to account for the closing corner?
    area = inner + (outer // 2) + 1

    return area


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    pos = (0, 0)
    nodes = []
    outer = 0
    for line in puzzle_input:
        _, _, color = line.strip().split()
        hex_instr, d = color[2:7], color[7]
        d = int(d)
        dir = ["R", "D", "L", "U"][d]
        steps = int(hex_instr, 16)
        # count the circumference of the area
        outer += steps

        # only capture the nodes, not any walls in between
        pos = (pos[0] + DIRS[dir][0] * steps, pos[1] + DIRS[dir][1] * steps)
        nodes.append(pos)

    inner = shoelace(nodes)
    area = inner + (outer // 2) + 1

    return area


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/18.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 13:00 End: 18:54 (with long break)
# Part 2: Start: 18:55 End:

# Elapsed time to run part1: 0.00085 seconds.
# Part 1: 40131
# Elapsed time to run part2: 0.00098 seconds.
# Part 2: 104454050898331
