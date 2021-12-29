# Load any required modules. Most commonly used:

import re
from itertools import product, combinations
# from collections import defaultdict
from utils.aoctools import aoc_timer

ROTATION = {
    0: (0, 1, 2),
    1: (1, 2, 0),
    2: (2, 0, 1),
    3: (1, 0, 2),
    4: (2, 1, 0),
    5: (0, 2, 1)}


class Beacon:
    def __init__(self, id, x, y, z) -> None:
        self.id = id
        self.coords = (x, y, z)

    def __repr__(self) -> str:
        return f'({self.id}): {self.coords}'


class Scanner:
    def __init__(self, id: int, beacons: list[Beacon]) -> None:
        self.id = id
        self.beacons = {b.id: b for b in beacons}
        self.pattern = self.generate_pattern()

    def __repr__(self) -> str:
        return f'[{self.id}]: {self.beacons}'

    def generate_pattern(self):
        """Generate the relative pattern of beacons seen by the scanner,
        represented by the Manhattan distance from each beacon to all other beacons.
        """
        pattern_dict = dict()
        for b in self.beacons.values():
            b_distances = []
            for o in self.beacons.values():
                if b != o:
                    b_distances.append(dist(b.coords, o.coords))

            pattern_dict[b.id] = sorted(b_distances)

        return pattern_dict


def dist(s: tuple[int], o: tuple[int]):
    """Manhattan distance between two (x, y, z) coordinates."""
    return (abs(s[0] - o[0]) + abs(s[1] - o[1]) + abs(s[2] - o[2]))


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    puzzle_input = []
    regex = re.compile(r'(-?\d+)')
    with open(f_name, 'r') as f:
        sections = f.read().split('\n\n')
        for s in sections:
            lines = s.strip().split('\n')
            # find the scanner ID in the first line
            m = regex.search(lines[0])
            if m:
                id = int(m[0])
            beacons = []
            for i, line in enumerate(lines[1:]):
                beacons.append(
                    Beacon(i, *list(map(int, regex.findall(line.strip())))))
            scanner = Scanner(id, beacons)
            puzzle_input.append(scanner)

    return puzzle_input


def find_matching_beacons(s: Scanner, t: Scanner):
    """Find a list of matching beacons between two scanners.

    Returns a list of tuples with matching beacon IDs for scanners s and t.
    """
    matching_ids = []
    for b in s.pattern:
        for c in t.pattern:
            matches = set(s.pattern[b]) & set(t.pattern[c])
            if len(matches) >= 8:
                # print(
                #     f'{matches}: {b} == {c} ({s.pattern[b]} == {t.pattern[c]})')
                matching_ids.append((b, c))

    return matching_ids


def find_scanner_coords(s: Scanner, t: Scanner, matching_ids: list[tuple[int]]):
    """Find the coordinates of scanner t relative to scanner s (which is assumed to be at (0, 0, 0)).

    Returns:
    - converted (x, y, z)
    - rotation required to match s's rotation
    - directions for (x, y, z) required to match s's directions
    """
    for c in ROTATION:
        for p in product([-1, 1], repeat=3):
            # all combinations of products of how to calculate (s.x - t.x) (8)
            xs = {s.beacons[s_id].coords[0] + p[0] *
                  t.beacons[t_id].coords[ROTATION[c][0]] for s_id, t_id in matching_ids}
            ys = {s.beacons[s_id].coords[1] + p[1] *
                  t.beacons[t_id].coords[ROTATION[c][1]] for s_id, t_id in matching_ids}
            zs = {s.beacons[s_id].coords[2] + p[2] *
                  t.beacons[t_id].coords[ROTATION[c][2]] for s_id, t_id in matching_ids}
            if len(xs) == 1 and len(ys) == 1 and len(zs) == 1:
                # found a matching configuration
                return ((xs.pop(), ys.pop(), zs.pop()), c, p)


def relative_coords(from_coords: tuple[int], to_coords: tuple[int], rot: int, direction: tuple[int]):
    """Calculate coordinates of a position 'from' (x, y, z) (can be a beacon or scanner position) 
    relative to 'to', using 'to''s rotation, direction and position relative to (0, 0, 0) 
    (no rotation and direction (1, 1, 1)).

    To calculate coordinates of scanner 1's beacons in scanner 0 coordinates, pass in:
    - from_coords: scanner 1's beacon's coordinates
    - to_coords: scanner 1's coordinates relative to scanner 0
    - rotation and direction from conversions[(from, to)]
    """
    rot_coords = ROTATION[rot]
    dir_factor = direction
    return (to_coords[0] - dir_factor[0] * from_coords[rot_coords[0]],
            to_coords[1] - dir_factor[1] * from_coords[rot_coords[1]],
            to_coords[2] - dir_factor[2] * from_coords[rot_coords[2]])


def convert_coords(from_id: int, to_id: int, coords: list[tuple[int]], conversions: dict):
    """Convert a list of (x, y, z) coordinates from coordinates relative to 'from' to 'to' reference.

    E.g. coordinate all beacons from coord in scanner 1 to scanner 0 relative coordinates.
    """
    ref_coords, rot, direction = conversions[(from_id, to_id)]
    results = []
    for c in coords:
        x = relative_coords(c, ref_coords, rot, direction)
        results.append(x)

    return results


@aoc_timer
def part1(puzzle_input: list[Scanner]) -> int:
    """Solve part 1. Return the required output value."""

    scanners = puzzle_input[:]
    unique_beacons = set()

    # find matching beacons between all scanners
    matching_beacons = dict()
    for s, t in combinations(puzzle_input, 2):
        matching_ids = find_matching_beacons(s, t)
        if len(matching_ids) >= 12:
            matching_beacons[(s.id, t.id)] = matching_ids
            # add reverse list for the reverse pair (t, s)
            matching_beacons[(t.id, s.id)] = [(t, s) for s, t in matching_ids]

    # generate conversions for each overlapping scanners
    # dictionary keys:      [from_id, to_id]
    # dictionary values:    ((from_coords in to_reference), rotation_required to "from" coordinates,
    #                        (x, y, z)-factor to be applied for direction)
    conversions = dict()
    for s, t in matching_beacons:
        t_coords, rot, direction = find_scanner_coords(
            scanners[s], scanners[t], matching_beacons[(s, t)])
        conversions[(t, s)] = (t_coords, rot, direction)

    # create a log of all scanner coordinates in s0 coordinates
    scanner_coordinates = dict()

    # How to convert coordinates from one system to another,
    # based on the conversion dictionary:
    #
    # To convert s4 coordinates (in s1 coordinates) into s0 coordinates:
    # take coords (s) from coversion[(4, 1)]
    # take coords (r), rot, direction from conversion[(1, 0)]
    # then run into relative_coords(s, r, rot, direction)
    #
    # s4_coords, _, _ = conversions[(4, 1)]
    # s1_coords, rot, direction = conversions[(1, 0)]
    # x = relative_coords(s4_coords, s1_coords, rot, direction)
    #
    # For a beacon, take the beacon coordinates and convert them first from
    # their current reference (s4) into s1, then into s0.

    # Starting from scanner 0, run a BFS across all conversion paths to convert all scanners and
    # beacons to 0 coordinates
    q = [(0, [], (0, 0, 0))]
    seen = set()
    while q:
        current_scanner, current_path, current_coords = q.pop(0)
        if current_scanner in seen:
            continue

        seen.add(current_scanner)
        # convert beacons along conversion path
        x = [b.coords for b in scanners[current_scanner].beacons.values()]
        s = [current_coords]
        for from_id, to_id in current_path:
            x = convert_coords(from_id, to_id, x, conversions)
            # Part 2: convert scanner coordinates itself - only if a conversion for the scanner to the next stage
            # does not yet exist (e.g. for (1, 0), there is already a converted value in conversions)
            if (current_scanner, to_id) not in conversions:
                s = convert_coords(from_id, to_id, s, conversions)
        for b in x:
            unique_beacons.add(b)
        # add current scanner coordinates in s0 notation
        scanner_coordinates[current_scanner] = s[0]

        for pair in [p for p in conversions if p[1] == current_scanner]:
            if pair[0] not in seen:
                q.append(
                    (pair[0], [pair] + current_path, conversions[pair][0]))

    # Part 2, calculate manhattan distance for each pair of scanners
    max_dist = 0
    max_pair = None
    for s in scanner_coordinates:
        for t in scanner_coordinates:
            if s != t:
                d = dist(scanner_coordinates[s], scanner_coordinates[t])
                if d > max_dist:
                    max_dist = d
                    max_pair = (s, t)

    print(f'Part 2: Max distance: {max_dist}')
    print(f'Pair: {max_pair}')

    return len(unique_beacons)


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/19.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

# Part 1: Start: 12:14 End: 15:00 (next day - this was hard!)
# Part 2: Start: 15:00 End: 15:23 (easy)

# Elapsed time to run part1: 3.50741 seconds.
# Part 1: 390
# Part 2: Max distance: 13327
# Pair: (12, 9)
