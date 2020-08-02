import hashlib
from collections import deque

inp = 'vwbaicqe'

ex0 = 'hijkl'
ex1 = 'ihgpwlah' # DDRRRD
ex2 = 'kglvqrro' # DDUDRLRRUDRD
ex3 = 'ulqzkmiv' # DRURDRUDDLLDLUURRDULRLDUUDDDRR


# this will require a BFS for sure... 
# the nodes in the graph will be
# - coordinates of the room
# - path
# if i reach a room along the same path, i have already been there?
# what about the first four letters of the hash
# - coordinates of the room
# - hash


# functions required

# generate the MD5 hash and return the first 4 characters
def gen_md5_hash(s):
    return hashlib.md5(s.encode()).hexdigest()[:4]

# we don't need to generate the grid, it is simple as we are always starting at (0, 0) 
# and ending at (3, 3)

# get valid neighbours based on
# - passcode
# - path
# - current position
def get_neighbors(passcode, path, cur_pos):
    doors = gen_md5_hash(passcode + path)
    # doors are in order: 
    # up, down, left, right
    neighbors = []
    for door, move_pos, direction in zip(doors, [(-1, 0), (1, 0), (0, -1), (0, 1)], 'UDLR'):
        next_pos = (cur_pos[0] + move_pos[0], cur_pos[1] + move_pos[1])
        if door in 'bcdef' and 0 <= next_pos[0] < 4 and 0 <= next_pos[1] < 4:
            neighbors.append((next_pos, direction))
    return neighbors


# BFS code
start = (0, 0)
target = (3, 3)
seen = set()
q = deque([(start, '')])
paths = []

# change the passcode here to run through examples...
passcode = inp

# this flag is used to print the first answer found (shortest path) for part 1
part1 = True

while q:
    cur_pos, cur_path = q.popleft()

    if (cur_pos, cur_path) in seen:
        continue

    seen.add((cur_pos, cur_path))

    if cur_pos == target:
        paths.append(cur_path)
        # we found a path to the target room, print out a message if it si the first path
        # for part 1
        if part1:
            print(f'Found the shortest path to the target, path: {cur_path}')
            part1 = False
        # skip all neighbors from here as we ended at the target. Start with rest of queue
        # otherwise this will create an endless loop
        continue

    # get neighbors and add to queue
    for next_pos, direction in get_neighbors(passcode, cur_path, cur_pos):
        # do we need to check here if the next step and path to it is shorter than one seen previously?
        # Don't think so as we can return to the same spot multiple times and new doors might open
        q.append((next_pos, cur_path + direction))


# we're done (either got stuck or found the target room)
print('Done.')
if paths:
    longest_path = sorted(paths, reverse=True, key=len)[0]
    print(f'Longest path length: {len(longest_path)}')

# part 1: DRDRULRDRD
# part 2: 384
