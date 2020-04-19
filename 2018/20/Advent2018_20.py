example1 = '^ENWWW(NEEE|SSE(EE|N))$' # 10 doors
example2 = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$' # 18 doors
example3 = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$' # 23 doors
example4 = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$' # 31 doors

example0 = '^WNE$'  # 3 doors

# use solution from mrFred489 at https://www.reddit.com/r/adventofcode/comments/a7uk3f/2018_day_20_solutions/
from collections import defaultdict

# directions
directions = {
                'N': (0, -1),
                'E': (1, 0),
                'S': (0, 1),
                'W': (-1, 0)
}

# stack to track current position
positions = []
# starting positions
x, y = 5000, 5000
# previous positions
pre_x, pre_y = x, y
# distance tracking dictionary
distances = defaultdict(int)
# starting distance
dist = 0

########## set input
f = open(r'input.txt').read().rstrip()
maze = f

for c in maze[1:-1]:
    print('Char: %s, stack: %d' % (c, len(positions)))
    if c == '(':   # save position if we find a new branch
        positions.append((x, y))
    elif c == ')': # end of branch, pop position before branch
        x, y = positions.pop()
    elif c == '|': # option, go back to last position but leave on stack
                   # until we find the closing ')'
        x, y = positions[-1]
    else:          # process door
        dx, dy = directions[c] # get direction change
        x += dx
        y += dy
        # add to distance (distance for current position)
        if distances[(x, y)] != 0:  # we already have a distance entry - we were here already
            # take the minimum since there is a shorter route to the room
            distances[(x, y)] = min(distances[(x, y)], distances[(pre_x, pre_y)] + 1)
        else:  # new room, add previous distance plus 1
            distances[(x, y)] = distances[(pre_x, pre_y)] + 1

    pre_x, pre_y = x, y

# show max distance - part 1
print(max(distances.values()))
# rooms with > 1000 doors distance
print(len([x for x in distances.values() if x >= 1000]))