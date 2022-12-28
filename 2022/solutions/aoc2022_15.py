# Load any required modules. Most commonly used:

import re

# from collections import defaultdict
# from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    regex = re.compile(r"(-?\d+)")
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            matches = regex.findall(line.strip())
            if matches:
                puzzle_input.append(list(map(int, matches)))

    return puzzle_input


def get_sensor_beacon_positions(puzzle_input):
    """Convert the puzzle input (4 integers) into a dictionary:
    (x, y) of sensor: (x, y) of beacon
    """
    return {(xs, ys): (xb, yb) for xs, ys, xb, yb in puzzle_input}


def manhattan_distance(x1, y1, x2, y2) -> int:
    """Calculate Manhattan distance between two points"""
    return abs(x1 - x2) + abs(y1 - y2)


def print_grid(positions, covered):
    all_coordinates = set(positions.keys()) | set(positions.values()) | covered
    min_x = min(all_coordinates, key=lambda c: c[0])[0]
    max_x = max(all_coordinates, key=lambda c: c[0])[0]
    min_y = min(all_coordinates, key=lambda c: c[1])[1]
    max_y = max(all_coordinates, key=lambda c: c[1])[1]

    for y in range(min_y, max_y + 1):
        line = f"{y:5} "
        for x in range(min_x, max_x + 1):
            if (x, y) in positions.keys():
                c = "S"
            elif (x, y) in positions.values():
                c = "B"
            elif (x, y) in covered:
                c = "#"
            else:
                c = "."
            line += c
        print(line)


# @aoc_timer
def part1(puzzle_input, y=2_000_000):
    """Solve part 1. Return the required output value.

    In the row where y=2_000_000, how many positions cannot contain a beacon?
    """
    positions = get_sensor_beacon_positions(puzzle_input)
    covered = set()
    print("Initial map")
    print_grid(positions, covered)
    for (xs, ys), (xb, yb) in positions.items():
        print(f"Calculating coverage for s:({xs}, {ys}) b:({xb}, {yb})")
        # calculate manhattan distance around each sensor
        md = manhattan_distance(xs, ys, xb, yb)
        print(f"Manhattan distance: {md}")
        # add positions in that area to a set of covered coordinates
        for yc in range(-md, 1):
            for xc in range(-md - yc, md + yc + 1):
                covered.add((xs + xc, ys + yc))

        for yc in range(1, md + 1):
            for xc in range(-md + yc, md - yc + 1):
                covered.add((xs + xc, ys + yc))
        # count the covered coordinates in the row
        print_grid(positions, covered)
    result = sum(
        1 for xc, yc in covered if yc == y and (xc, yc) not in positions.values()
    )

    print("End result")
    print_grid(positions, covered)

    return result


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/15.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start:  End:
# Part 2: Start:  End:
