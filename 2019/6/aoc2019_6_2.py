from collections import defaultdict, deque

f_name = 'input.txt'

with open(f_name) as f:
    orbits = [l.strip('\n').split(')') for l in f.readlines()]

#### part 2
# use BFS to find shortest path


# generate graph with all neighbours for each node
neighbours = defaultdict(list)
for a, b in orbits:
    neighbours[a].append(b)
    neighbours[b].append(a)

def BFS(graph, start):
    q = deque([(start, [])])
    seen = set()
    path = defaultdict(list)
    while q:
        v1, p = q.pop() # removes element from the right side of the queue
        if v1 not in seen:
            seen.add(v1)
            
            # find all valid neighbours
            for v_next in graph[v1]:
                if (v_next not in seen 
                    and v_next not in path):
                    # push into queue - on the left side
                    # set the path to this new square
                    path[v_next] = p + [v_next]
                    q.appendleft((v_next, p + [v_next]))
                  
    # once q is empty, return the dictionary with paths
    return path

start = 'YOU'
end = 'SAN'

path = BFS(neighbours, start)

print('Shortest path from {} to {} is {}, length {}'.format(start, end, path[end], len(path[end]) - 2))

# part 2 solution is 307