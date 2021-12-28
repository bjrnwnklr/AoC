# Load any required modules. Most commonly used:

import re
from itertools import product
# from collections import defaultdict
# from utils.aoctools import aoc_timer

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
        # self.x = x
        # self.y = y
        # self.z = z

    # def __eq__(self, __o: object) -> bool:
    #     return self.x == __o.x and self.y == __o.y and self.z == __o.z

    # def __lt__(self, __o: object) -> bool:
    #     return sum([self.x, self.y, self.z]) < sum([__o.x, __o.y, __o.z])

    def __repr__(self) -> str:
        return f'({self.id}): {self.coords()}'

    def dist(self, o: 'Beacon'):
        """Manhattan distance to another beacon."""
        return (abs(self.coords[0] - o.coords[0]) + abs(self.coords[1] - o.coords[1]) + abs(self.coords[2] - o.coords[2]))

    # def coords(self):
    #     return (self.x, self.y, self.z)


class Scanner:
    def __init__(self, id: int, beacons: list[Beacon]) -> None:
        self.id = id
        self.beacons = {b.id: b for b in beacons}
        # self.x = 0
        # self.y = 0
        # self.z = 0
        # self.rotation = 0
        # self.direction = (1, 1, 1)
        self.pattern = self.generate_pattern()

    def __repr__(self) -> str:
        return f'[{self.id}]: {self.beacons}'

    # def coords(self):
    #     return (self.x, self.y, self.z)

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
            matches = sum(1 for n in s.pattern[b] if n in t.pattern[c])
            if matches >= 11:
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
    print(
        f'finding scanner coordinates conversion: {s.id} -> {t.id}, {matching_ids}')
    for c in ROTATION:
        for p in product([-1, 1], repeat=3):
            # all combinations of products of how to calculate (s.x - t.x) (8)
            # ys = {s.beacons[s_id].coords[1] + p[1] *
            #       getattr(t.beacons[t_id], ROTATION[c][1]) for s_id, t_id in matching_ids}
            xs = {s.beacons[s_id].coords[0] + p[0] *
                  t.beacons[t_id].coords[ROTATION[c][0]] for s_id, t_id in matching_ids}
            ys = {s.beacons[s_id].coords[1] + p[1] *
                  t.beacons[t_id].coords[ROTATION[c][1]] for s_id, t_id in matching_ids}
            zs = {s.beacons[s_id].coords[2] + p[2] *
                  t.beacons[t_id].coords[ROTATION[c][2]] for s_id, t_id in matching_ids}
            # print(f'{c=}, {p=}: {len(xs)=} {len(ys)=} {len(zs)=}')
            if len(xs) == 1 and len(ys) == 1 and len(zs) == 1:
                # we found a matching configuration
                # print(f'Matching config found: {c=}, {p=}')

                return ((xs.pop(), ys.pop(), zs.pop()), c, p)


def relative_coords(r: tuple[int], s: tuple[int], rot: int, direction: tuple[int]):
    """Calculate coordinates of a position s (x, y, z) (can be a beacon or scanner position) 
    relative to r, using r's rotation, direction and position relative to (0, 0, 0) 
    (no rotation and direction (1, 1, 1)).

    To calculate coordinates of scanner 4 relating to scanner 0 (0, 0, 0) coordinates
    by using scanner 1's relative coordinates, pass in
    scanner 1s coordinates (rel to scanner 1) as r and
    scanner 4s coordinates (rel to scanner 1) as s.
    """
    c = ROTATION[rot]
    p = direction
    return (r[0] - p[0] * s[c[0]],
            r[1] - p[1] * s[c[1]],
            r[2] - p[2] * s[c[2]])
    # return (r[c[0]] - p[0] * s[0],
    #         r[c[1]] - p[1] * s[1],
    #         r[c[2]] - p[2] * s[2])
    # return (getattr(r, c[0]) - p[0] * s[0],
    #         getattr(r, c[1]) - p[1] * s[1],
    #         getattr(r, c[2]) - p[2] * s[2])

    # @aoc_timer


def part1(puzzle_input: list[Scanner]) -> int:
    """Solve part 1. Return the required output value."""

    scanners = puzzle_input[:]
    unique_beacons = set()

    # for b in s0.beacons:
    #     unique_beacons.add(s0.beacons[b].coords)

    # find matching beacons between all scanners
    matching_beacons = dict()
    for s in puzzle_input:
        for t in puzzle_input:
            if s.id != t.id:
                matching_ids = find_matching_beacons(s, t)
                if len(matching_ids) >= 12:
                    matching_beacons[(s.id, t.id)] = matching_ids
                    print(
                        f'Matching beacons found between {s.id} and {t.id}: {len(matching_ids)}')

    print(matching_beacons)

    # try some conversions for the scanner coordinates
    conversions = dict()
    for s, t in matching_beacons:
        t_coords, rot, direction = find_scanner_coords(
            scanners[s], scanners[t], matching_beacons[(s, t)])
        conversions[(s, t)] = (t_coords, rot, direction)

    print('Conversion dictionary:')
    for k, v in conversions.items():
        print(k, v)

    # convert coordinates of s4 via s1 to s0 reference
    # result should be: -20,-1133,1061
    print('S4 coordinates converted via s1 to s0:')
    s, _, _ = conversions[(1, 4)]
    r, rot, direction = conversions[(0, 1)]
    x = relative_coords(r, s, rot, direction)
    print(x)

    # convert coordinates of s3 via s1 to s0 reference
    # result should be: -92,-2380,-20
    print('S3 coordinates converted via s1 to s0:')
    s, _, _ = conversions[(1, 3)]
    r, rot, direction = conversions[(0, 1)]
    x = relative_coords(r, s, rot, direction)
    print(x)

    # convert coordinates of s2 via s4 to s1 and then to s0 reference
    # result should be: 1105,-1205,1229
    print('S2 coordinates converted via s4 to s1:')
    s, _, _ = conversions[(4, 2)]
    r, rot, direction = conversions[(1, 4)]
    x = relative_coords(r, s, rot, direction)
    print(x)
    print('S2 coordinates converted via s1 to s0:')
    # s, _, _ = conversions[(4, 2)]
    r, rot, direction = conversions[(0, 1)]
    x = relative_coords(r, x, rot, direction)
    print(x)

    # this is the correct conversion:
    # To convert s4 coordinates (relate to s1) into s0 coordinates:
    # take coords (s) from coversion[(1, 4)]
    # take coords (r), rot, direction from conversion[(0, 1)]
    # then run into relative_coords(r, s, rot, direction)
    #
    # s4_coords, _, _ = conversions[(1, 4)]
    # s1_coords, rot, direction = conversions[(0, 1)]
    # x = relative_coords(s1_coords, s4_coords, rot, direction)

    # Convert 2 to 4 to 1 to 0:
    # x=-1205, p=1 * a=-1246 + q=-1 * b=72 + r=1 * c=113
    # x=1229, p=-1 * a=-1104 + q=1 * b=168 + r=1 * c=-43
    # x=1105, p=-1 * a=-1125 + q=1 * b=68 + r=-1 * c=88

    # # find matching beacons
    # matching_ids = find_matching_beacons(s0, s1)
    # # add the first set of matching beacons to the list - using the coordinates relative to scanner 0
    # find_scanner_coords(s0, s1, matching_ids)

    # # try to convert s1's beacons to s0 coordinates
    # for b in s1.beacons:
    #     print(
    #         f's1 Beacon converted to s0 coordinates: ({b}) {s1.beacons[b].coords()} -> {relative_coords(s1, s1.beacons[b].coords())}')

    # # try again with scanner 1 vs scanner 4
    # s4 = puzzle_input[4]
    # matching_ids = find_matching_beacons(s1, s4)
    # find_scanner_coords(s1, s4, matching_ids)
    # print()
    # print(f'Scanner 4 coordinates, relative to scanner 1: {s4.coords()}')
    # s4_coords = relative_coords(s1, s4.coords())
    # print(f'Scanner 4 coordinates, relative to scanner 0: {s4_coords}')
    # # now need to convert coordinates relative to scanner 1 to scanner 0

    # TODO: Convert ALL beacons of all scanners into s0 coordinates, then put into a set to match.

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
