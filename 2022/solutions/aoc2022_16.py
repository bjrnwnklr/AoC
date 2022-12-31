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


def heuristic_move(minute, to_node, ov, valves, eruption):
    """Use the estimated time * flow of the next room valve as heuristic.
    If the valve is already open, return 0.
    """
    if to_node in ov:
        return 0

    return valves[to_node] * (eruption - (minute + 2))


def heuristic_open(minute, node, valves, eruption):
    """Use the estimated time * flow of the current node's valve as heuristic"""
    return valves[node] * (eruption - (minute + 1))


def astar(graph, valves):
    q = [(0, 1, "AA", "", ["AA"])]
    cost_so_far = {("AA", ""): 0}
    eruption = 30

    while q:
        _, minute, node, ov, path = heapq.heappop(q)
        print(f"Popped heapq: {minute=} {node=} {ov=} {path=}")
        # print(f"{q=}")

        if minute == eruption:
            print("Found solution:")
            print(f"Flow achieved: {cost_so_far[(node, ov)]}")
            print(f"Open valves: {ov}")
            print("Path:")
            for n in path:
                print(n)
            return cost_so_far[(node, ov)]

        # for next steps, we have two options
        # - move to next node (increase minute by one, leave cost as is)
        # - open valve (increase minute by one, increase cost by minute * flow)
        for next_node in graph[node]:
            new_cost = cost_so_far[(node, ov)]
            if (next_node, ov) not in cost_so_far or new_cost > cost_so_far[
                (next_node, ov)
            ]:
                cost_so_far[(next_node, ov)] = new_cost
                priority = new_cost + heuristic_move(
                    minute, next_node, ov, valves, eruption
                )
                heapq.heappush(
                    q,
                    (
                        -priority,
                        minute + 1,
                        next_node,
                        ov,
                        path
                        + [
                            next_node,
                        ],
                    ),
                )

        if node not in ov:
            new_cost = cost_so_far[(node, ov)] + heuristic_open(
                minute, node, valves, eruption
            )
            cost_so_far[(node, open_valve(ov, node))] = new_cost
            priority = new_cost
            heapq.heappush(
                q,
                (
                    -priority,
                    minute + 1,
                    node,
                    open_valve(ov, node),
                    path
                    + [
                        f"Open valve {node}",
                    ],
                ),
            )

    return -1


def dijkstra(graph, valves):
    q = [(0, 1, "AA", "", ["AA"])]
    seen = set()
    eruption = 30

    while q:
        cost, minute, node, ov, path = heapq.heappop(q)
        print(f"Popped heapq: {minute=} {cost=} {node=} {ov=} {path=}")
        # print(f"{q=}")
        if (node, ov) in seen:
            continue

        seen.add((node, ov))

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
                    cost,
                    minute + 1,
                    next_node,
                    ov,
                    path
                    + [
                        next_node,
                    ],
                ),
            )
            # if the valve of the next node is not open, add the step to open
            # it to the queue
            if next_node not in ov:
                heapq.heappush(
                    q,
                    (
                        cost - (valves[next_node] * (eruption - (minute + 2))),
                        minute + 2,
                        next_node,
                        open_valve(ov, next_node),
                        path
                        + [
                            next_node,
                            f"Open valve {next_node}",
                        ],
                    ),
                )

        if node not in ov:
            heapq.heappush(
                q,
                (
                    cost - (valves[node] * (eruption - (minute + 1))),
                    minute + 1,
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
    # heapq needs to compare cost at minute against each other, otherwise, it will
    # prioritize lower cost at the beginning
    result = dijkstra(graph, valves)
    # result = astar(graph, valves)

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
