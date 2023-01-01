# Load any required modules. Most commonly used:

import re

from collections import defaultdict

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


def find_distances(graph):
    """Run a BFS starting from each valve to determine distance
    (in minutes) to each other valve. Return a dictionary with
    (from, to): distance in minutes."""
    distances = dict()
    for from_valve in graph:
        q = [(from_valve, 0)]
        seen = set()

        while q:
            curr_valve, distance = q.pop(0)

            if curr_valve in seen:
                continue

            seen.add(curr_valve)
            if (from_valve, curr_valve) not in distances or distance < distances[
                (from_valve, curr_valve)
            ]:
                distances[(from_valve, curr_valve)] = distance

            for next_valve in graph[curr_valve]:
                if next_valve not in seen:
                    q.append((next_valve, distance + 1))

    return distances


def open_valve(ov, valve):
    """Store state of valves opened in a text string.

    Order does not matter so sort them alphabetically.
    """
    already_visited = ov.split(",")
    return ",".join(
        sorted(
            already_visited
            + [
                valve,
            ]
        )
    )


def bfs(graph, valves, distances, duration):
    q = [(0, 0, "AA", "")]
    flow_per_state = {}

    while q:
        cost, minute, node, ov = q.pop(0)

        # store cost for this state
        if ov in flow_per_state:
            if cost > flow_per_state[ov]:
                flow_per_state[ov] = cost
        else:
            flow_per_state[ov] = cost

        # next nodes are valves we can still open within the remaining time
        # - distances between valves are stored in the `distances` dictionary
        # - which valves are open already is stored in the `ov` string
        # get all possible valves that can still be opened
        # (include the current node as it is not opened when we start - we might
        #  want to open it)
        neighbors = [
            n
            for n in graph
            if n not in ov
            and valves[n] > 0
            and (minute + distances[(node, n)] + 1) < duration
        ]
        for next_node in neighbors:
            # check that we have not yet visited the node,
            # and that we have enough time
            # to move to the valve and open it (+1 minute)
            new_ov = open_valve(ov, next_node)
            new_minute = minute + distances[(node, next_node)] + 1
            if new_minute <= duration:
                q.append(
                    (
                        cost + (valves[next_node] * (duration - new_minute)),
                        new_minute,
                        next_node,
                        new_ov,
                    ),
                )

    return flow_per_state


# @aoc_timer
def part1(valves, graph):
    """Solve part 1. Return the required output value.

    The nodes are really only the valves being opened in a certain order.
    The cost of travel between valve openings is the distance (1 minute per node)
    that's required to go to the next valve and open it.

    First determine the distance between all nodes by running a BFS
    from each node across the graph and build a dictionary.

    Then use Dijkstra to find the path to 30 minutes that has the highest flow.
    """
    # get all distances in the graph
    distances = find_distances(graph)

    # run a Dijkstra search, maximizing the cost (negative cost)
    # Cost is the number of remaining minutes * flow
    # goal is reached at 30 minutes
    # store status of valves (open / closed) as they are the different states
    # heapq needs to compare cost at minute against each other, otherwise, it will
    # prioritize lower cost at the beginning
    flow_per_state = bfs(graph, valves, distances, 30)
    max_flow = max(flow_per_state.values())

    return max_flow


# @aoc_timer
def part2(valves, graph):
    """Solve part 2. Return the required output value.

    Time: 26 minutes.
    Instead of one person moving to open valves, there are now 2
    (you and one elephant).

    Great solution building on mine (BFS)
    https://www.reddit.com/r/adventofcode/comments/zo21au/comment/j0nz8df/?utm_source=share&utm_medium=web2x&context=3
    """
    # get all distances in the graph
    distances = find_distances(graph)

    # run a Dijkstra search, maximizing the cost (negative cost)
    # Cost is the number of remaining minutes * flow
    # goal is reached at 30 minutes
    # store status of valves (open / closed) as they are the different states
    # heapq needs to compare cost at minute against each other, otherwise, it will
    # prioritize lower cost at the beginning
    flow_per_state = bfs(graph, valves, distances, 26)
    max_flow = max(flow_per_state.values())

    return max_flow


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

# Part 1: 2320
# Part 2: NOT 2963 (too low!)
