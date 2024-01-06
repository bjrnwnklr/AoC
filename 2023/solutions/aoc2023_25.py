# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import random
from copy import deepcopy

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


def karger(graph):
    """Run Karger's algorithm on the graph and return
    the number of cuts and the nodes in both partitions."""
    # dictionary to count how many nodes have been consolidated
    # into each contracted node
    node_count = defaultdict(lambda: 1)
    while len(graph) > 2:
        # randomly select an edge - in this case, select
        # node v randomly, and then one of w's neighbors randomly
        # since the graph is defined by the list of edges between nodes
        v = random.choice(list(graph.keys()))
        w = random.choice(graph[v])
        # contract the edge by consolidating the nodes
        contract(graph, v, w)
        node_count[v] += node_count[w]

    # count the number of remaining edges between the two remaining nodes
    v = list(graph.keys())[0]
    w = graph[v][0]
    mincut = len(graph[v])
    return mincut, node_count[v], node_count[w]


def contract(graph, v, w):
    """Contract two nodes together and repoint the edges between them."""
    for node in graph[w]:
        # repoint all neighbors from w to v instead
        if node != v:
            # avoid repointing itself in a loop
            graph[v].append(node)
            graph[node].append(v)
        # remove node from neighbors of w, we have to also
        # do this for v
        graph[node].remove(w)
    # now completely remove the node w from the graph
    del graph[w]


@aoc_timer
def part1_karger(puzzle_input):
    """Solve part 1 by implementing Karger's algorithm to find the minimum cut
    between two partitions in the graph."""
    # parse the input into a graph of connected nodes
    g = defaultdict(list)
    for line in puzzle_input:
        left, right = line.split(":")
        for r in right.split():
            g[left].append(r)
            g[r].append(left)

    cut = 0
    while cut != 3:
        gg = deepcopy(g)
        cut, partition1, partition2 = karger(gg)

    print(
        f"Finished Karger: Cut: {cut}, Elements per partition: {partition1}, {partition2}"
    )

    return partition1 * partition2


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # parse the input into a graph of connected nodes
    g = defaultdict(list)
    G = nx.Graph()
    for line in puzzle_input:
        left, right = line.split(":")
        for r in right.split():
            g[left].append(r)
            g[r].append(left)
            G.add_edge(left, r)

    # nx.draw_networkx(G, with_labels=True)
    # plt.savefig("2023_25.png")

    # calculate communities using Girvan Newman Algorithm,
    # which splits graph iteratively into communities by
    # removing the edge with the highest score
    communities = nx.community.girvan_newman(G)
    first_community = next(communities)
    print("Number of communities: ", len(first_community))
    print("Elements per community: ", [len(c) for c in first_community])
    result = 1
    for l in (len(c) for c in first_community):
        result *= l

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/25.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 1 using Karger's algo and print the answer
    p2 = part1_karger(puzzle_input)
    print(f"Part 1 with Karger's algorithm: {p2}")

# Part 1: Start: 15:43 End: 16:55
# Part 2: Start:  End:

# Elements per community:  [754, 733]
# Elapsed time to run part1: 13.17160 seconds.
# Part 1: 552682
# Finished Karger: Cut: 3, Elements per partition: 733, 754
# Elapsed time to run part1_karger: 1.40319 seconds.
# Part 1 with Karger's algorithm: 552682 Part 1: 552682
