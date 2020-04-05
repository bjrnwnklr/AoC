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

# data types used - namedtuple comes in very handy here
# GC = grid cell, consisting of numeric value and operator
# CP = current position, consisting of row, column and weight
GC = namedtuple('GC', ['num', 'op'])
CP = namedtuple('CP', ['r', 'c', 'w'])

# find valid neighbors
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

# move to the position given by `n` and update the weight of the orb accordingly
def move(cp, op, n):
    # update position
    r = n[0]
    c = n[1]
    w = cp.w
    # calculate new weight if we are on a number cell
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
        # update operator since we are on an operator cell
        op = gc.op

    return CP(r, c, w), op

# the grid with numbers and operators.
# _ is the meaningless operator used where are on a cell with a number
# 0 is the number when we stand on a cell with an operator
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




# do a BFS from start point to (3, 3, 30)
start = CP(0, 0, 22)
goal = CP(3, 3, 30)

# BFS queue contains 
# - start position
# - current operator
# - list of steps (empty)
q = deque([(start, '_', [])])
seen = set()

# simple BFS
while(q):
    current_pos, current_op, current_path = q.pop()

    if current_pos not in seen:
        seen.add(current_pos)

    # if we found a solution, check if it is valid (i.e. we only went to the last room exactly once)
    # and stop if we found a valid solution
    if current_pos == goal:
        # check that we only accept solutions that visited the last room exactly once!
        if current_path.count((3, 3)) == 1:
            print(f'Found solution: {current_pos}, {current_path}')
            break
        else:
            # not a valid solution, so move on to next queue element
            continue
        
    # add next steps to the queue
    for n in get_neighbors((current_pos.r, current_pos.c)):
        next_pos, next_op = move(current_pos, current_op, n)
        q.appendleft((next_pos, next_op, current_path + [n]))


