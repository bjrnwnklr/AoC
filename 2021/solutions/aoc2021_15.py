# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer
from heapq import heappush, heappop


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(list(map(int, list(line.strip()))))

    return puzzle_input


def neighbors(g, pos):
    results = []
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        nr = pos[0] + dr
        nc = pos[1] + dc
        if (nr, nc) in g:
            results.append((nr, nc))
    return results


def dijkstra(g, start, target):
    """Run a Dijkstra search for the shortest path in the grid"""
    q = [(0, start)]
    seen = set()
    while q:
        (cost, cur_pos) = heappop(q)
        if cur_pos not in seen:
            seen.add(cur_pos)
            if cur_pos == target:
                return cost

            for next_pos in neighbors(g, cur_pos):
                if next_pos not in seen:
                    heappush(q, (cost + g[next_pos], next_pos))


def generate_grid(inp):
    return {(r, c): val
            for r, row in enumerate(inp)
            for c, val in enumerate(row)
            }


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    g = generate_grid(puzzle_input)
    target = (len(puzzle_input) - 1, len(puzzle_input[0]) - 1)
    result = dijkstra(g, (0, 0), target)

    return result


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/15.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 19:01 End: 19:21
# Part 2: Start: 19:22 End:
