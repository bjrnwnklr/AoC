#### Day 17 - Reservoir Research
from collections import defaultdict


def print_map(grid, min_x, max_x, min_y, max_y, water):
    for y in range(0, min_y):
        print(''.join('+' if (x, y) == water else '.' for x in range(min_x - 1, max_x + 2)))
    for y in range(min_y, max_y + 1):
        print(''.join(grid[(x, y)] for x in range(min_x - 1, max_x + 2)))
    print('\n')
    

def process(q, grid, x, y, d):
    """
    Process grid element and update the grid at position (x, y) accordingly.
    Process sideways if necessary (both left and right)
    """
    
    below = grid[(x, y + 1)]
    
    print('Current: (%d, %d, %d)' % (x, y, d))
    #print_map(grid, min_x, max_x, min_y, max_y, water)

    if min_x <= x <= max_x and min_y <= y <= max_y:
        # assume water falling from above
        if below == '.':
            grid[(x, y)] = '|'
            n = neighbour(x, y, d)
            if n:
                q.append((x, y + d, d))
            else:
                return False
        elif below == '#':
            # branch left and right now
            grid[(x, y)] = '~'
            # go left
            l = x - 1
            while ((l, y) not in clay and (l, y) in grid):
                if grid[(l, y + 1)] == '#' or grid[(l, y + 1)] == '~':
                    grid[(l, y)] = '~'
                else:
                    grid[(l, y)] = '|'
                    q.append((l, y + 1, 1))
                    break
                l -= 1
            # go right
            r = x + 1
            while (r, y) not in clay and (r, y) in grid:
                if grid[(r, y + 1)] == '#' or grid[(r, y + 1)] == '~':
                    grid[(r, y)] = '~'
                else:
                    grid[(r, y)] = '|'
                    q.append((r, y + 1, 1))
                    break
                r += 1
            # change direction
            d *= -1
            q.append((x, y + d, d))
        elif below == '~':
            # we are most likely going up
            left_bound = True
            right_bound = True
            # go left
            l = x - 1
            ############ need to add something here to first check if there are any
            # borders. if yes, fill all the way to borders. Otherwise don't fill at all
            # This is required to check for a second flow of water coming from above,
            # which currently adds a new row of water on the top.
            while ((l, y) not in clay and (l, y) in grid):
                if grid[(l, y + 1)] == '#' or grid[(l, y + 1)] == '~':
                    grid[(l, y)] = '~'
                else:
                    grid[(l, y)] = '|'
                    left_bound = False
                    q.append((l, y + 1, 1))
                    break
                l -= 1
            # go right
            r = x + 1
            while (r, y) not in clay and (r, y) in grid:
                if grid[(r, y + 1)] == '#' or grid[(r, y + 1)] == '~':
                    grid[(r, y)] = '~'
                else:
                    grid[(r, y)] = '|'
                    right_bound = False
                    q.append((r, y + 1, 1))
                    break
                r += 1
            if left_bound and right_bound:
                grid[(x, y)] = '~'
                q.append((x, y + d, d))
    else:
        return False    

def neighbour(x, y, d):
    return (x, y + d, d) if (x, y + d) not in clay and (x, y + d) in grid else False


# read example
f = open('input.txt', 'r')

# coordinates are format (x, y) = (c, r)

clay = set()
for l in f:
    a, b = l.split(', ')
    a_val = int(a[2:])
    b_1, b_2 = map(int, b[2:].split('..'))
    for i in range(b_1, b_2 + 1):
        if a[0] == 'x':
            #grid[(a_val, i)] = '#'
            clay.add((a_val, i))
        else:
            #grid[(i, a_val)] = '#'
            clay.add((i, a_val))

min_y = min(y for _, y in clay)
max_y = max(y for _, y in clay)
min_x = min(x for x, _ in clay)
max_x = max(x for x, _ in clay)
print(min_x, max_x, min_y, max_y)

g = {(x, y) : '#' if (x, y) in clay else '.'
        for x in range(min_x - 1, max_x + 2)
        for y in range(min_y, max_y + 1)}

grid = defaultdict(lambda: '.', g)
water = (500, 0)
q = [(500, min_y, 1)]

#print_map(grid, min_x, max_x, min_y, max_y, water)
while q:
    next_x, next_y, direction = q.pop()
    process(q, grid, next_x, next_y, direction)

result = sum(1 for x, y in grid.keys() if grid[(x, y)] == '~' or grid[(x, y)] == '|' if min_y <= y <= max_y)
print(result)

print_map(grid, min_x, max_x, min_y, max_y, water)
