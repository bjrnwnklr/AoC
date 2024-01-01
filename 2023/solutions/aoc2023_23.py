# Load any required modules. Most commonly used:

# import re
from collections import defaultdict, deque
from heapq import heappop, heappush

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


SLOPES = {">": 0, "v": 1, "<": 2, "^": 3}


def parse_grid(puzzle_input):
    """Parse the grid into a number of outputs:

    - set of non-walkable positions (forest)
    - dictionary of slopes: (r, c): [<^>v]
    - starting position
    - end position
    """
    walls = set()
    slopes = dict()
    for r, row in enumerate(puzzle_input):
        for c, cell in enumerate(row):
            if cell == "#":
                walls.add((r, c))
            elif cell in ["<", ">", "^", "v"]:
                slopes[(r, c)] = SLOPES[cell]

    start = (0, 1)
    end = (len(puzzle_input) - 1, len(puzzle_input[0]) - 2)

    return walls, slopes, start, end


def dijkstra(puzzle_input, part2=False):
    """Find the longest path in the grid using a BFS."""
    walls, slopes, start, end = parse_grid(puzzle_input)
    steps = defaultdict(int)
    paths = defaultdict(list)
    # (steps, position, direction we come from)
    # direction: 0: right, 1: down, 2: left, 3: up
    # assume we start coming down, but doesnt matter
    q = [(0, start, 1)]
    while q:
        curr_steps, curr_pos, prev_dir = heappop(q)
        curr_steps *= -1

        # only continue if the current path is longer than what
        # we have already used to get to this point
        if curr_steps < steps[(curr_pos, prev_dir)]:
            continue
        steps[(curr_pos, prev_dir)] = curr_steps

        # don't need to check for end position, we just explore
        # the whole grid and then return the step count for the
        # end position
        for direction, (dr, dc) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            rr, cc = curr_pos[0] + dr, curr_pos[1] + dc
            # valid next steps are:
            # - not a wall
            # - within the grid
            # - not yet visited during current path
            # Additionally, if it is a slope, it needs to be in
            # the same direction as we are walking.
            if (
                (rr, cc) not in walls
                and 0 <= rr <= end[0]
                and 0 <= cc <= end[1]
                and (rr, cc) not in paths[(curr_pos, prev_dir)]
            ):
                if part2 or ((rr, cc) not in slopes or direction == slopes[(rr, cc)]):
                    paths[((rr, cc), direction)] = paths[(curr_pos, prev_dir)] + [
                        (rr, cc)
                    ]
                    heappush(q, (-(curr_steps + 1), (rr, cc), direction))

    return steps[(end, 1)]


def scan_nodes(puzzle_input):
    """Find intersections (between slopes) and generate a graph between
    the nodes."""
    walls, slopes, start, end = parse_grid(puzzle_input)
    # node: [(node, length)]
    graph = defaultdict(set)
    q = deque([(start, start, 0)])
    seen = set()
    while q:
        curr_pos, curr_node, curr_steps = q.popleft()
        if (curr_pos, curr_node) in seen:
            continue
        seen.add((curr_pos, curr_node))

        # generate next steps and check if they are surrounded by slopes:
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            rr, cc = curr_pos[0] + dr, curr_pos[1] + dc
            if (rr, cc) not in walls and 0 <= rr <= end[0] and 0 <= cc <= end[1]:
                # check if current position is surrounded by slopes
                next_node = curr_node
                next_steps = curr_steps + 1
                if (rr, cc) == end:
                    # end position counts as a node, so add.
                    graph[curr_node].add(((rr, cc), next_steps))
                    graph[(rr, cc)].add((curr_node, next_steps))
                    next_node = (rr, cc)
                    next_steps = 0
                else:
                    slope_count = 0
                    for nr, nc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        slope_pos = (rr + nr, cc + nc)
                        if slope_pos not in walls and slope_pos in slopes:
                            slope_count += 1

                    if slope_count >= 2 and curr_node != (rr, cc):
                        # found a position surrounded by slopes
                        graph[curr_node].add(((rr, cc), next_steps))
                        graph[(rr, cc)].add((curr_node, next_steps))
                        next_node = (rr, cc)
                        next_steps = 0

                q.append(((rr, cc), next_node, next_steps))

    return graph


def bfs_part2(graph, start, end):
    """Run a BFS on the graph of grid nodes (intersections)
    and find the longest path from start to end."""
    steps = []
    seen = set()
    # current node, total steps, path
    q = deque([(start, 0, [start])])
    while q:
        curr_node, curr_steps, curr_path = q.popleft()
        seen.add((curr_node, curr_steps))

        if curr_node == end:
            steps.append(curr_steps)

        for next_node, next_steps in graph[curr_node]:
            if next_node not in curr_path:
                q.append((next_node, curr_steps + next_steps, curr_path + [next_node]))

    return max(steps)


def print_grid(puzzle_input, path):
    """Print the path taken through the grid"""
    print()
    for r, row in enumerate(puzzle_input):
        line = ""
        for c, cell in enumerate(row):
            if (r, c) in path:
                line += "0"
            else:
                line += cell
        print(line)


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    result = dijkstra(puzzle_input)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    graph = scan_nodes(puzzle_input)
    _, _, start, end = parse_grid(puzzle_input)
    result = bfs_part2(graph, start, end)

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/23.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 13:09 End: 13:44
# Part 2: Start: 13:51 End: 17:15

# Elapsed time to run part1: 1.40956 seconds.
# Part 1: 2294
# Elapsed time to run part2: 73.65117 seconds.
# Part 2: 6418
