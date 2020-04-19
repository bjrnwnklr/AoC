from collections import defaultdict
import heapq

result = []
instr = defaultdict(list)
dep = defaultdict(list)

with open(r'input1.txt') as f:
    for l in f:
        x = l.split(' ')
        instr[x[1]].append(x[7])
        dep[x[7]].append(x[1])

# find all starting values that don't have dependencies
s = [x for x in instr if x not in dep]

# topological sort with a heapq for alphabetical order
while s:
    # pick next element without any dependencies
    cur = heapq.heappop(s)
    # and add it to the results
    result.append(cur)

    # now take next node which depends on current element
    for m in instr[cur]:
        # and remove the edge from cur to m
        dep[m].remove(cur)
        # if m has no more incoming edges (all dependencies fulfilled),
        # add it to the heapq
        if not dep[m]:
            heapq.heappush(s, m)

print(''.join(result))
