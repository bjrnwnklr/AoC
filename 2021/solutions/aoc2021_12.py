# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append([x for x in line.strip().split('-')])

    return puzzle_input


def build_graph(inp):
    """Build a bi-directional graph from the puzzle input."""
    g = defaultdict(list)
    for a, b in inp:
        g[a].append(b)
        g[b].append(a)

    return g


def bfs(g: defaultdict(list)) -> list:
    """Run a Breadth First Search on the provided bi-directional graph and return
    a list of possible paths from 'start' to 'end'.

    Rules followed: 
    - small caves (small letters) can only be visited once.
    - large caves (capital letters) can be visited any number of times.
    """
    q = [('start', 'start', set())]
    target = 'end'
    # this will only hold small caves, large caves can be visited multiple times.
    paths = []

    while q:
        cur_node, cur_path, cur_seen = q.pop(0)
        if cur_node in cur_seen:
            continue

        if cur_node.islower():
            cur_seen.add(cur_node)

        if cur_node == target:
            # we have reached the end, add the path to the list of found paths
            paths.append(cur_path)

        for next_node in g[cur_node]:
            if next_node not in cur_seen:
                q.append((next_node, cur_path + ',' +
                         next_node, cur_seen.copy()))

    return paths


def bfs2(g: defaultdict(list), small_cave: str) -> list:
    """Run a Breadth First Search on the provided bi-directional graph and return
    a list of possible paths from 'start' to 'end'.

    Rules followed: 
    - one small cave (small letters) can be visited twice.
    - all other small caves (small letters, incl 'start' and 'end') can only be visited once.
    - large caves (capital letters) can be visited any number of times.
    """
    q = [('start', 'start', set(), False)]
    target = 'end'
    # this will only hold small caves, large caves can be visited multiple times.
    paths = []

    while q:
        cur_node, cur_path, cur_seen, scvisited = q.pop(0)
        if cur_node in cur_seen:
            continue

        if cur_node.islower():
            if cur_node == small_cave and not scvisited:
                scvisited = True
            else:
                cur_seen.add(cur_node)

        if cur_node == target:
            # we have reached the end, add the path to the list of found paths
            paths.append(cur_path)

        for next_node in g[cur_node]:
            if next_node not in cur_seen:
                q.append((next_node, cur_path + ',' +
                          next_node, cur_seen.copy(), scvisited))

    return paths


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    g = build_graph(puzzle_input)
    paths = bfs(g)

    return len(paths)


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    paths = []
    g = build_graph(puzzle_input)

    # get all small letters in the graph
    small_caves = [x for x in g if x.islower() and x not in ['start', 'end']]

    for small_cave in small_caves:
        paths += bfs2(g, small_cave)

    return len(set(paths))


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/12.txt')
    # puzzle_input = load_input('testinput/12_1_1.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 17:39 End: 18:15
# Part 2: Start: 18:21 End: 19:04
