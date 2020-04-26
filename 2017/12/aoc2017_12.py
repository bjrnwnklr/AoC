from collections import defaultdict

f_name = 'input.txt'

graph = defaultdict(list)


with open(f_name, 'r') as f:
    for line in f:
        left, right = line.strip('\n').split(' <-> ')
        for r in right.split(', '):
            graph[left].append(r)
            # graph[r].append(left)


# collect all elements into a set
all_members = set(graph.keys())

# traverse the graph from 0 using a simple BFS
# set of nodes that belong to group 0
seen = set()
q = ['0']

while q:
    curr = q.pop(0)
    if curr in seen:
        continue

    seen.add(curr)

    for n in graph[curr]:
        q.append(n)

print(f'Done, {len(seen)} members in group 0: {seen}.')

# part 1: 239

# part 2 - pick an elements from all members, then traverse the graph and remove each element
groups = []
while all_members:
    # get the first element and start BFS with it
    first_element = sorted(all_members)[0]

    # now run BFS on it
    seen = set()
    q = [first_element]

    while q:
        curr = q.pop(0)
        if curr in seen:
            continue

        seen.add(curr)
        all_members.remove(curr)

        for n in graph[curr]:
            q.append(n)

    # now add the set of seen (= 1 group) to groups
    groups.append(seen)

# done, count number of groups
print(f'Number of groups found: {len(groups)}')

# part 2: 215 groups found