from collections import deque

def dist(a, b):
    d = sum(abs(a[i] - b[i]) for i in range(4))
    return True if d < 4 else False


def in_range(b):
    r = 3
    br = {(b[0] + x, b[1] + y, b[2] + z, b[3] + j) for x in range(-r, r + 1)
                                         for y in range(-(r - x), r - x + 1)
                                         for z in range(-(r - y), r - y + 1)
                                         for j in range(-(r - z), r - z + 1)
                                         if abs(x) + abs(y) + abs(z) + abs(j) <= r}
    return br


coords = set()
for l in open(r'input.txt').readlines():
    coords.add(tuple(map(int, l.strip().split(','))))

# find neighbours for each coordinate
neighbours = dict()
for c in coords:
    neighbours[c] = coords & in_range(c)


# create constellations by starting with one coordinate
# mark coordinates as seen when in constellation
seen = set()
constellations = []
# start with biggest neighbourhood
for c in sorted(coords, key = lambda x: len(neighbours[x]), reverse = True):
    
    if c not in seen:
        queue = deque([c])
        constellation = set()
        seen.add(c)

        while queue:
            cur = queue.pop()
            constellation |= neighbours[cur]
            for n in neighbours[cur]:
                if n not in seen:
                    queue.appendleft(n)
                    seen.add(n)
        # all neighbours processed, add constellation to list of constellations
        constellations.append(constellation)

print(constellations)
print(len(constellations))