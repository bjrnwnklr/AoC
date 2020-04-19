from collections import defaultdict
import heapq

result = []
instr = defaultdict(list)
dep = defaultdict(list)
wq = []                 # worker queue
t = 0

with open(r'input.txt') as f:
    for l in f:
        x = l.split(' ')
        instr[x[1]].append(x[7])
        dep[x[7]].append(x[1])

# find all starting values that don't have dependencies
s = sorted([x for x in instr if x not in dep])

# topological sort with a heapq for alphabetical order
while wq or s:
    # fill the worker queue
    while len(wq) < 5 and s:
         cur = heapq.heappop(s)
         print('Worker queue starting at %s, t = %d' % (cur, t))
         heapq.heappush(wq, (t + 60 + ord(cur) - 64, cur))

    t, x = heapq.heappop(wq)
    # and add it to the results
    result.append(x)

    # now take next node which depends on current element
    for m in instr[x]:
        # and remove the edge from cur to m
        dep[m].remove(x)
        # if m has no more incoming edges (all dependencies fulfilled),
        # add it to the heapq
        if not dep[m]:
            heapq.heappush(s, m)

print('time: %d' % t)
print(''.join(result))
