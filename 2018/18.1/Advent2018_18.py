## Advent 18
from collections import defaultdict

def count_adj(x, y, g):
    s = sum(1 for i in range(x-1, x+2) 
            for j in range(y-1, y+2)
            if (i, j) != (x, y)  
            and grid[(i, j)] == g)
    #print('%s: %d' % (g, s))
    return s
  
def print_grid():
    for i in range(max_y+1):
        s = ''.join(grid[(j, i)] for j in range(max_x+1))
        print(s)

def process(grid_temp):
    for i in range(max_y+1):
        for j in range(max_x+1):
            new_val = grid[(j, i)]
            if new_val == '.':
                if count_adj(j, i, '|') >= 3:
                    new_val = '|'
            elif new_val == '|':
                if count_adj(j, i, '#') >= 3:
                    new_val = '#'
            elif new_val == '#':
                if count_adj(j, i, '#') < 1 or count_adj(j, i, '|') < 1:
                    new_val = '.'
            grid_temp[(j, i)] = new_val

def calc_value():
    woods = sum(1 for g in grid.values() if g == '|')
    lumberyards = sum(1 for g in grid.values() if g == '#')
    return(woods, lumberyards, woods * lumberyards)

# open input
f = open('input.txt', 'r')

grid = defaultdict(str)
grid_temp = defaultdict(str)

for y, l in enumerate(f):
    for x, g in enumerate(l):
        grid[(x, y)] = g
        max_x = x
    max_y = y

results = [0] # add one element to represent minute 0 (initial state)
for i in range(1, 470): # start at 1 representing 1 minute for 1st iter
    process(grid_temp)
    grid = grid_temp.copy()
    grid_temp.clear()
    w, l, v = calc_value()
    if v in results:
        v_1 = results.index(v)
        print('%d - repeat result also at %d: %d' % (i, v_1, v))
    results.append(v)
    #print('%d: %d woods * %d lumberyards = %d. Delta: %d' % (i, w, l, v, v-d))


###### part 2
# values start repeating after some time every 28 minutes
# repeats start at 407 with 208750
# and repeat from 435 (28 minutes later)

target = 1000000000
offset = ((target - 407) % 28) + 407
part2 = results[offset]
print('part 2: %d at %d' % (part2, offset))

## result is 196310 at offset 412