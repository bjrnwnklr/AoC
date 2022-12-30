# Load any required modules. Most commonly used:

import re
from tqdm import tqdm

# from collections import defaultdict
from utils.aoctools import aoc_timer


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
    """Convert the puzzle input (4 integers) into a list of tuples:
    (x, y) of sensor, (x, y) of beacon, manhattan distance
    """
    return [
        (xs, ys, xb, yb, manhattan_distance(xs, ys, xb, yb))
        for xs, ys, xb, yb in puzzle_input
    ]


def manhattan_distance(x1, y1, x2, y2) -> int:
    """Calculate Manhattan distance between two points"""
    return abs(x1 - x2) + abs(y1 - y2)


def consolidate(intervals):
    """Consolidate a list of intervals using a stack"""
    stack = []
    # sort intervals by left boundary
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    # push first interval onto stack
    if sorted_intervals:
        stack.append(sorted_intervals[0])
    for i in range(1, len(sorted_intervals)):
        current = sorted_intervals[i]
        # if current interval overlaps (i.e. left side is lower than stack's right side)
        # update stack's right side to max of current and stack
        if current[0] <= stack[-1][1]:
            stack[-1] = (stack[-1][0], max(stack[-1][1], current[1]))
        else:
            stack.append(current)

    return stack


def count_length(intervals):
    """Count how many positions are in a list of intervals
    (incl start and stop of each interval)."""
    result = 0
    for i in intervals:
        result += i[1] - i[0] + 1

    return result


@aoc_timer
def part1(puzzle_input, y=2_000_000):
    """Solve part 1. Return the required output value.

    In the row where y=2_000_000, how many positions cannot contain a beacon?
    """
    positions = get_sensor_beacon_positions(puzzle_input)
    intervals = []
    for xs, ys, xb, yb, md in tqdm(positions):
        # Calculate this only for line y, i.e. only add positions
        # that are in line y. Do not iterate if line y is not included.
        if ys - md <= y <= ys + md + 1:
            yc = abs(ys - y)
            intervals.append((xs + (-md + yc), xs + md - yc))

    # remove existing beacons if they overlap with any of the intervals
    num_beacons_overlap = 0
    beacons = set((xb, yb) for _, _, xb, yb, _ in positions)
    for xb, yb in set(beacons):
        if yb == y:
            intervals.append((xb, xb))
            num_beacons_overlap += 1
    # consolidate intervals
    cons_intervals = consolidate(intervals)

    # count items in covered (all positions in the line we are looking for)
    # and subtract the number of beacons in that line (some beacons) are referenced
    # multiple times in the coordinates so take a set
    result = count_length(cons_intervals) - num_beacons_overlap

    return result


@aoc_timer
def part2(puzzle_input, max_xy=4_000_000):
    """Solve part 2. Return the required output value.
    you need to determine its tuning frequency,
    which can be found by multiplying its x coordinate by
    4_000_000 and then adding its y coordinate.
    """
    # this implementation builds intervals for each line to check.
    # This takes ca 30 seconds to find the only position free within the lines
    # A much shorter implementation can be achieved:
    # - if the position of the missing beacon is the only free space on the line,
    #   it has to be within distance of d+1 (d == manhattan distance between sensor and
    #   beacon) of multiple sensors
    # - check all d+1 positions for every sensor and eliminate the ones that
    #   are not within the target square, and that are covered by another sensor
    # - see Jonathan Paulson's solution
    positions = get_sensor_beacon_positions(puzzle_input)
    for row in tqdm(range(max_xy + 1)):
        intervals = []
        for xs, ys, xb, yb, md in positions:
            # Calculate this only for the desired row, i.e. only add positions
            # that are in line row. Do not iterate if line row is not included.
            if ys - md <= row <= ys + md + 1:
                # offset of the row from the current sensor, used to calculate
                # length of the row
                yc = abs(ys - row)
                # calculate left and right side and check if within target square
                left = xs + (-md + yc)
                right = xs + md - yc
                if not ((right < 0) or (left > max_xy)):
                    # add interval within the target square
                    intervals.append((max(0, left), min(right, max_xy)))

        # add existing beacons if they overlap with any of the intervals
        num_beacons_overlap = 0
        beacons = set((xb, yb) for _, _, xb, yb, _ in positions)
        for xb, yb in set(beacons):
            if yb == row:
                intervals.append((xb, xb))
                num_beacons_overlap += 1
        # consolidate intervals
        cons_intervals = consolidate(intervals)

        # check if the length of the covered range is different from a full line
        # of the target square, i.e. if there is a space left - which has to be
        # the beacon
        if len(cons_intervals) > 1:
            # more than one element in the list of intervals
            # should not be more than 2.
            assert len(cons_intervals) == 2
            col = cons_intervals[0][1] + 1
            break

    result = col * 4_000_000 + row
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

# Elapsed time to run part1: 0.01006 seconds.
# Part 1: 5508234
# Elapsed time to run part2: 23.29471 seconds.
# Part 2: 10457634860779
