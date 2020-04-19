from collections import defaultdict

f_name = 'input.txt'

with open(f_name) as f:
    orbits = [l.strip('\n').split(')') for l in f.readlines()]

o_count = defaultdict(int)
graph = defaultdict(list)

# get dictionary of predecesors and successors
for a, b in orbits:
    graph[a].append(b)

"""
for x in graph:
    print(x, graph[x])
"""
start = 'COM'

def count_graph(graph, start):
    successors = graph[start]
    for s in successors:
        o_count[s] = o_count[start] + 1
        count_graph(graph, s)

count_graph(graph, start)

"""
for x in graph:
    print(x, o_count[x])
"""

print('Part 1: ', sum(o_count.values()))

# Part 1 solution: 204521