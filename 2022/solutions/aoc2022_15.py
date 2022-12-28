# Load any required modules. Most commonly used:

import re
from tqdm import tqdm

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


def consolidate(intervals):
    """Consolidate a list of intervals using a stack"""
    stack = []
    # sort intervals by left boundary
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    print(f"Sorted intervals: {sorted_intervals}")
    # push first interval onto stack
    if sorted_intervals:
        stack.append(sorted_intervals.pop(0))
    while sorted_intervals:
        current = sorted_intervals.pop(0)
        # if current interval overlaps (i.e. left side is lower than stack's right side)
        # update stack's right side to max of current and stack
        if current[0] <= stack[-1][1]:
            stack[-1] = (stack[-1][0], max(stack[-1][1], current[1]))
        else:
            stack.append(current)
        print(f"Added {current} to stack: {stack}")

    return stack


def count_length(intervals):
    """Count how many positions are in a list of intervals
    (incl start and stop of each interval)."""
    result = 0
    for i in intervals:
        result += i[1] - i[0] + 1

    return result


# @aoc_timer
def part1(puzzle_input, y=2_000_000):
    """Solve part 1. Return the required output value.

    In the row where y=2_000_000, how many positions cannot contain a beacon?
    """
    positions = get_sensor_beacon_positions(puzzle_input)
    intervals = []
    for (xs, ys), (xb, yb) in tqdm(positions.items()):
        # calculate manhattan distance around each sensor
        md = manhattan_distance(xs, ys, xb, yb)
        print(f"Calculating interval for s:({xs}, {ys}) b:({xb}, {yb}). {md=}")
        # add positions in that area to a set of covered coordinates
        # Calculate this only for line y, i.e. only add positions
        # that are in line y. Do not iterate if line y is not included.
        if ys - md <= y <= ys + md + 1:
            yc = abs(ys - y)
            # add interval to list of intervals
            print(
                f"Interval overlaps with row {y}. Adding interval ({xs + (-md + yc)}, {xs + md - yc})"
            )
            intervals.append((xs + (-md + yc), xs + md - yc))

    print(f"Intervals: {intervals}")
    # remove existing beacons if they overlap with any of the intervals
    num_beacons_overlap = 0
    for xb, yb in set(positions.values()):
        if yb == y:
            intervals.append((xb, xb))
            num_beacons_overlap += 1
    print(f"Intervals with beacons: {intervals}")
    # consolidate intervals
    cons_intervals = consolidate(intervals)
    print(f"Consolidated intervals: {cons_intervals}")

    # count items in covered (all positions in the line we are looking for)
    # and subtract the number of beacons in that line (some beacons) are referenced
    # multiple times in the coordinates so take a set
    result = count_length(cons_intervals) - num_beacons_overlap

    return result


# @aoc_timer
def part2(puzzle_input, max_xy=4_000_000):
    """Solve part 2. Return the required output value.
    you need to determine its tuning frequency,
    which can be found by multiplying its x coordinate by
    4_000_000 and then adding its y coordinate.
    """
    positions = get_sensor_beacon_positions(puzzle_input)
    # square = {(x, y) for y in range(max_xy + 1) for x in range(max_xy + 1)}
    square = set()
    for (xs, ys), (xb, yb) in tqdm(positions.items()):
        # calculate manhattan distance around each sensor
        md = manhattan_distance(xs, ys, xb, yb)
        # print(f"Checking s:({xs}, {ys}) b:({xb}, {yb}). MD = {md}")
        # add positions in that area to a set of covered coordinates
        # Calculate this only for line y, i.e. only add positions
        # that are in line y. Do not iterate if line y is not included.
        if not ((max_xy < ys - md) or (0 > ys + md)) and not (
            (max_xy < xs - md) or (0 > xs + md)
        ):
            # print(f"Overlap with (0, {max_xy}), (0, {max_xy})")
            for dy in range(-md, md + 1):
                row = ys + dy
                # print(f"{dy=}, {row=}")
                # print(
                #     f"Checking row {row} and xc in range {xs + (-md + abs(dy))} .. {xs + (md - abs(dy) + 1)}"
                # )
                for xc in range(-md + abs(dy), md - abs(dy) + 1):
                    # if ((xs + xc, row)) in square:
                    square.add((xs + xc, row))

    # count items in covered (all positions in the line we are looking for)
    # and subtract the number of beacons in that line (some beacons) are referenced
    # multiple times in the coordinates so take a set
    for xb, yb in set(positions.values()):
        # if (xb, yb) in square:
        # square.remove((xb, yb))
        square.add((xb, yb))

    # square should only have one member now
    # print(square)
    print(len(square))
    # assert len(square) == 1

    beacon = square.pop()
    result = beacon[0] * 4_000_000 + beacon[1]

    return result


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
