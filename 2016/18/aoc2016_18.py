

f_name = 'input.txt'
# f_name = 'ex2.txt'
# number of rows to produce
n = 400000


def get_prev_row(grid, r, c):
    # max_cols = len(grid[0])

    # get left neighbor
    if c-1 < 0:
        ln = '.'
    else:
        ln = grid[r-1][c-1]
    # get middle neighbor
    # cn = grid[r-1][c]
    # get right neighbor
    if c+1 >= max_cols:
        rn = '.'
    else:
        rn = grid[r-1][c+1]
    # return (ln, cn, rn)
    return ln, rn

def is_trap(grid, r, c):
    # ln, cn, rn = get_prev_row(grid, r, c)
    ln, rn = get_prev_row(grid, r, c)
    trap = False
    
    if ln == '^':
        # if the right one is not a trap, it doesn't matter what the middle one is - always a trap
        if rn == '.':
            trap = True
    else:
        # left is not a trap, so if right is a trap we have a trap (again doesn't matter what middle is)
        if rn == '^':
            trap = True

    return '^' if trap else '.'

# number of safe tiles
safe_count = 0
with open(f_name, 'r') as f:
    grid = [[x for x in f.readline().strip('\n')]]
    # print(''.join(grid[0]))
    safe_count += sum(1 for c in grid[0] if c == '.')

max_cols = len(grid[0])


# generate next row and print out each row
for r in range(1, n):
    new_row = [is_trap(grid, r, c) for c in range(max_cols)]
    grid.append(new_row)
    # print(''.join(new_row))
    safe_count += sum(1 for c in new_row if c == '.')

print(f'Safe tiles: {safe_count}')

# Part 1: 1963
# Part 2: 20009568