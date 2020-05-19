from collections import defaultdict
from heapq import heappop, heappush

f_name = 'input.txt'

components = defaultdict(set)

# each element only appears once (even if left and right are reversed)

# generate graph. Nodes are the left and right pin counts.
# The weight of an edge is the negative sum of the pins (negative because heapq finds the smallest element)
# format of the graph is:
# - key: node
# - value: (node, weight)
with open(f_name, 'r') as f:
    for line in f.readlines():
            l, r = map(int, line.strip('\n').split('/'))
            weight = -(l + r)
            components[l].add((r, weight))
            components[r].add((l, weight))

# run a Dijkstra algorithm to find the heaviest bridge possible, starting from 0
# in the queue: 
# - cost (starting at 0)
# - node (starting at 0)
# - previous node (starting at 0) - this is used to determine already used edges
# - path (starting with empty path)
q = [(0, 0, 0, ())]
weights = defaultdict(list)
while q:
    (cost, node, prev, path) = heappop(q)
    edge = (min(node, prev), max(node, prev))
    # important: check if it is in path, not in seen!
    if edge not in path:
        path += (edge, )
        weights[cost].append((path))

        for next_node, weight in components[node]:
            heappush(q, (cost + weight, next_node, node, path))

# once done, we can query the costs dictionary for the max value

max_weight = min(weights.keys())
print(f'Max weight {-max_weight} for path {weights[max_weight]}')

print(f'{len(weights)} different weights found.')
# for w in sorted(weights):
#     print(f'{w}: {weights[w]}')

# Part 1: 1859