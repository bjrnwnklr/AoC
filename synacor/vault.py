# use a DFS to find the goal
#
# data structures to be used:
# 1) grid
#       (r, c) = (num, op), e.g (1, 0) = (0, +)
# 2) current position
#       ((r, c), weight, op)
#
#

from collections import namedtuple

GC = namedtuple('GC', ['num', 'op'])
CP = namedtuple('CP', ['r', 'c', 'w', 'op'])

def get_neighbors(x):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r, c = x

    for n in neighbors:
        if (0 <= r + n[0] <= 3) and (0 <= c + n[1] <= 3):
            yield n

def move(cp, n):
    # update position
    r = n[0]
    c = n[1]
    w = cp.w
    op = cp.op
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

    return CP(r, c, w, op)

    



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



start = CP(0, 0, 22, '_')
for n in get_neighbors((0, 0)):
    cp_next = move(start, n)
    for n2 in get_neighbors((cp_next.r, cp_next.c)):
        print(move(cp_next, n2))



