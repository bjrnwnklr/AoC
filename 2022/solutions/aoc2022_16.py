# Load any required modules. Most commonly used:

import re

from collections import defaultdict
import heapq

# from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # unsigned ints
    regex_valves = re.compile(r"([A-Z]{2})")
    regex_rate = re.compile(r"(\d+)")

    valves = dict()
    graph = defaultdict(set)

    with open(f_name, "r") as f:
        for line in f.readlines():
            # generate graph of paths between valves
            matches = regex_valves.findall(line.strip())
            if matches:
                first_valve = matches[0]
                for m in matches[1:]:
                    graph[first_valve].add(m)
                    graph[m].add(first_valve)
            # generate dictionary of flow rates per valve
            matches = regex_rate.findall(line.strip())
            if matches:
                valves[first_valve] = int(matches[0])

    return valves, graph


def open_valve(ov, valve):
    valves = ov.split(",")
    return ",".join(sorted(valves + [valve]))


def dijkstra(graph, valves):
    q = [(1, 0, "AA", "", ["AA"])]
    seen = set()
    eruption = 30

    while q:
        minute, cost, node, ov, path = heapq.heappop(q)
        print(f"Popped heapq: {minute=} {cost=} {node=} {ov=} {path=}")
        print(f"{q=}")
        if (minute, node, ov) in seen:
            continue

        seen.add((minute, node, ov))

        # check if we arrived at the end
        if minute == eruption:
            print("Found solution:")
            print(f"Flow achieved: {cost}")
            print(f"Open valves: {ov}")
            print("Path:")
            for n in path:
                print(n)
            return -cost

        # for next steps, we have two options
        # - move to next node (increase minute by one, leave cost as is)
        # - open valve (increase minute by one, increase cost by minute * flow)
        for next_node in graph[node]:
            heapq.heappush(
                q,
                (
                    minute + 1,
                    cost,
                    next_node,
                    ov,
                    path
                    + [
                        next_node,
                    ],
                ),
            )

        if node not in ov:
            heapq.heappush(
                q,
                (
                    minute + 1,
                    cost - (valves[node] * (eruption - (minute + 1))),
                    node,
                    open_valve(ov, node),
                    path
                    + [
                        f"Open valve {node}",
                    ],
                ),
            )

    return -1


# @aoc_timer
def part1(valves, graph):
    """Solve part 1. Return the required output value."""
    # run a Dijkstra search, maximizing the cost (negative cost)
    # Cost is the number of remaining minutes * flow
    # goal is reached at 30 minutes
    # store status of valves (open / closed) as they are part of the different paths
    # heapq needs to compare cost at minute against each other, otherwise, it will prioritize lower cost at the beginning
    result = dijkstra(graph, valves)

    return result


# @aoc_timer
def part2(valves, graph):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    valves, graph = load_input("input/16.txt")

    # Solve part 1 and print the answer
    p1 = part1(valves, graph)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(valves, graph)
    print(f"Part 2: {p2}")

# Part 1: Start: 17:58 End:
# Part 2: Start:  End:
