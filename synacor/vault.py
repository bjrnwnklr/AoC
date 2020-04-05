# use a DFS to find the goal
#
# data structures to be used:
# 1) grid
#       (r, c) = (num, op), e.g (1, 0) = (0, +)
# 2) current position
#       ((r, c), weight, op)
#
#

from collections import namedtuple, deque

GC = namedtuple('GC', ['num', 'op'])
CP = namedtuple('CP', ['r', 'c', 'w'])

def get_neighbors(x):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r, c = x

    for n in neighbors:
        next_r = r + n[0]
        next_c = c + n[1]
        if (0 <= next_r <= 3) and (0 <= next_c <= 3):
            # avoid going back to the 0, 0 start
            if (next_r, next_c) != (0, 0):
                yield (next_r, next_c)

def move(cp, op, n):
    # update position
    r = n[0]
    c = n[1]
    w = cp.w
    # calculate new weight
    gc = grid[n]
    if gc.num != 0:
        if op == '+':
            w += gc.num
        elif op == '*':
            w *= gc.num
        elif op == '-':
            w -= gc.num
        op = '_'
    else:
        # update operator
        op = gc.op

    return CP(r, c, w), op

    



grid = {
    (0, 0): GC(22, '_'),
    (0, 1): GC(0, '-'),
    (0, 2): GC(9, '_'),
    (0, 3): GC(0, '*'),
    (1, 0): GC(0, '+'),
    (1, 1): GC(4, '_'),
    (1, 2): GC(0, '-'),
    (1, 3): GC(18, '_'),
    (2, 0): GC(4, '_'),
    (2, 1): GC(0, '*'),
    (2, 2): GC(11, '_'),
    (2, 3): GC(0, '*'),
    (3, 0): GC(0, '*'),
    (3, 1): GC(8, '_'),
    (3, 2): GC(0, '-'),
    (3, 3): GC(1, '_')
}



start = CP(0, 0, 22)
# for n in get_neighbors((0, 0)):
#     cp_next, op = move(start, '_', n)
#     print(cp_next, op)
#     for n2 in get_neighbors((cp_next.r, cp_next.c)):
#         print(move(cp_next, op, n2))


# do a BFS from start point to (3, 3, 30)
goal = CP(3, 3, 30)

# BFS queue contains 
# - start position
# - current operator
# - list of steps (empty)
q = deque([(start, '_', [])])

seen = set()

while(q):
    current_pos, op, current_path = q.pop()

    if current_pos not in seen:
        seen.add(current_pos)

    if current_pos == goal:
        print(f'Found solution: {current_pos}, {current_path}')
        

    for n in get_neighbors((current_pos.r, current_pos.c)):
        next_pos, next_op = move(current_pos, op, n)
        q.appendleft((next_pos, next_op, current_path + [n]))


