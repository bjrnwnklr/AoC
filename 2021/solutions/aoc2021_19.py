# Load any required modules. Most commonly used:

import re
from itertools import product
# from collections import defaultdict
# from utils.aoctools import aoc_timer

ROTATION = {
    0: ('x', 'y', 'z'),
    1: ('y', 'z', 'x'),
    2: ('z', 'x', 'y')}


class Beacon:
    def __init__(self, id, x, y, z) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

    def __lt__(self, __o: object) -> bool:
        return sum([self.x, self.y, self.z]) < sum([__o.x, __o.y, __o.z])

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def dist(self, o: object):
        """Manhattan distance to another beacon."""
        return (abs(self.x - o.x) + abs(self.y - o.y) + abs(self.z - o.z))

    def coords(self):
        return (self.x, self.y, self.z)


class Scanner:
    def __init__(self, id: int, beacons: list[Beacon]) -> None:
        self.id = id
        self.beacons = {b.id: b for b in beacons}
        self.x = 0
        self.y = 0
        self.z = 0
        self.rotation = 0
        self.direction = (1, 1, 1)
        self.pattern = self.generate_pattern()

    def __repr__(self) -> str:
        return f'[{self.id}]: {self.beacons}'

    def coords(self):
        return (self.x, self.y, self.z)

    def generate_pattern(self):
        """Generate the relative pattern of beacons seen by the scanner,
        represented by the Manhattan distance from each beacon to all other beacons.
        """
        pattern_dict = dict()
        for b in self.beacons.values():
            b_distances = []
            for o in self.beacons.values():
                if b != o:
                    b_distances.append(b.dist(o))

            pattern_dict[b.id] = sorted(b_distances)

        return pattern_dict


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
                id = m[0]
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
            matches = sum(1 for n in s.pattern[b] if n in t.pattern[c])
            if matches >= 11:
                # print(
                #     f'{matches}: {b} == {c} ({s.pattern[b]} == {t.pattern[c]})')
                matching_ids.append((b, c))

    return matching_ids


def find_scanner_coords(s: Scanner, t: Scanner, matching_ids: list[tuple[int]]):
    """Find the coordinates of scanner t relative to scanner s (which is assumed to be at (0, 0, 0))."""
    found = False
    while not found:
        for c in ROTATION:
            for p in product([-1, 1], repeat=3):
                # all combinations of products of how to calculate (s.x - t.x) (8)
                # TODO: probably also need to account for rotation by swapping x, y and z - should be 24 combinations to check
                xs = {s.beacons[s_id].x + p[0] *
                      getattr(t.beacons[t_id], ROTATION[c][0]) for s_id, t_id in matching_ids}
                ys = {s.beacons[s_id].y + p[1] *
                      getattr(t.beacons[t_id], ROTATION[c][1]) for s_id, t_id in matching_ids}
                zs = {s.beacons[s_id].z + p[2] *
                      getattr(t.beacons[t_id], ROTATION[c][2]) for s_id, t_id in matching_ids}
                if len(xs) == 1 and len(ys) == 1 and len(zs) == 1:
                    # we found a matching configuration
                    print(f'Matching config found: {c=}, {p=}')
                    # update position, rotation, direction of t
                    t.rotation = c
                    t.direction = p
                    t.x = xs.pop()
                    t.y = ys.pop()
                    t.z = zs.pop()
                    found = True
                    break


def relative_coords(r: Scanner, s):
    """Calculate coordinates of a position s (x, y, z) (can be a beacon or scanner position) 
    relative to r, using r's rotation, direction and position relative to (0, 0, 0) 
    (no rotation and direction (1, 1, 1)).

    To calculate coordinates of scanner 4 relating to scanner 0 (0, 0, 0) coordinates
    by using scanner 1's relative coordinates, pass in
    scanner 1s coordinates (rel to scanner 1) as r and
    scanner 4s coordinates (rel to scanner 1) as s.
    """
    c = ROTATION[r.rotation]
    p = r.direction
    return (getattr(r, c[0]) - p[0] * s[0],
            getattr(r, c[1]) - p[1] * s[1],
            getattr(r, c[2]) - p[2] * s[2])

    # @aoc_timer


def part1(puzzle_input: list[Scanner]) -> int:
    """Solve part 1. Return the required output value."""

    unique_beacons = set()

    s0 = puzzle_input[0]
    s1 = puzzle_input[1]

    # find matching beacons
    matching_ids = find_matching_beacons(s0, s1)
    # add the first set of matching beacons to the list - using the coordinates relative to scanner 0
    for m, _ in matching_ids:
        unique_beacons.add(s0.beacons[m].coords())
    find_scanner_coords(s0, s1, matching_ids)
    print()
    print(f'Scanner 1 coordinates: {s1.coords()}')
    print(f'Unique beacons so far: {unique_beacons}')

    # try again with scanner 1 vs scanner 4
    s4 = puzzle_input[4]
    matching_ids = find_matching_beacons(s1, s4)
    find_scanner_coords(s1, s4, matching_ids)
    print()
    print(f'Scanner 4 coordinates, relative to scanner 1: {s4.coords()}')
    s4_coords = relative_coords(s1, s4.coords())
    print(f'Scanner 4 coordinates, relative to scanner 0: {s4_coords}')
    # now need to convert coordinates relative to scanner 1 to scanner 0

    return 1


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/19.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 12:14 End:
# Part 2: Start:  End:
