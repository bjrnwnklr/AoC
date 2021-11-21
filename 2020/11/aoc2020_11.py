# f_name = 'ex1.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    grid = [[x for x in line.strip('\n')] for line in f.readlines()]

# save a copy of the grid for part 2
part2_grid = [[x for x in row] for row in grid]

# dimensions of the grid
WIDTH = len(grid[0])
HEIGHT = len(grid)


def get_occupied_seats(r, c):
    """
    Return the count of occupied seats around the given seat.
    :param r: row number of the seat to check
    :param c: column number of the seat to check
    :return: count of occupied seats surrounding the given seat.
    """
    occ_count = 0
    for i in [-1, 0, 1]:
        temp_r = r + i
        if 0 <= temp_r < HEIGHT:
            for j in [-1, 0, 1]:
                temp_c = c + j
                if (0 <= temp_c < WIDTH
                        and ((temp_r, temp_c) != (r, c))
                        and grid[temp_r][temp_c] == '#'):
                    occ_count += 1
    return occ_count


def print_grid(grid):
    for row in grid:
        print(''.join(x for x in row))


changed = True
cycles = 0
while changed:
    # iterate through each seat and generate a new state map
    temp_state = []
    changed = False
    for r in range(0, HEIGHT):
        temp_row = []
        for c in range(0, WIDTH):
            curr_val = grid[r][c]
            if curr_val == 'L':
                # check empty seat rule
                if get_occupied_seats(r, c) == 0:
                    curr_val = '#'
                    changed = True
            elif curr_val == '#':
                # check occupied seat rule
                if get_occupied_seats(r, c) >= 4:
                    curr_val = 'L'
                    changed = True
            temp_row.append(curr_val)
        temp_state.append(temp_row)

    # deep copy the temp_state grid
    grid = [[x for x in row] for row in temp_state]
    cycles += 1
    # print(f'[{cycles}]: Changed = {changed}')
    # print_grid(grid)

# we reached a stable state without any further changes
print(f'Part 1: Stable state reached after {cycles} cycles.')
# count occupied seats
occ_count = sum(1 for row in grid for seat in row if seat == '#')
print(f'Counted {occ_count} occupied seats.')


# part 1: 2204 occupied seats

# part 2

def get_pt2_occupied_seats(r, c):
    """
    Return the count of occupied seats around the given seat, following rules for part 2
    - first seat in each direction
    :param r: row number of the seat to check
    :param c: column number of the seat to check
    :return: count of occupied seats surrounding the given seat.
    """
    occ_count = 0
    for dir in [
        (-1, 0),  # up
        (-1, 1),  # up-right
        (0, 1),  # right
        (1, 1),  # down-right
        (1, 0),  # down
        (1, -1),  # down-left
        (0, -1),  # left
        (-1, -1)  # up-left
    ]:
        found = False
        factor = 1
        temp_r = r + dir[0]
        temp_c = c + dir[1]
        while 0 <= temp_r < HEIGHT and 0 <= temp_c < WIDTH and not found:
            if grid[temp_r][temp_c] == '#':
                occ_count += 1
                found = True
            elif grid[temp_r][temp_c] == 'L':
                found = True
            factor += 1
            temp_r = r + dir[0] * factor
            temp_c = c + dir[1] * factor
    return occ_count


grid = [[x for x in row] for row in part2_grid]
changed = True
cycles = 0
while changed:
    # iterate through each seat and generate a new state map
    temp_state = []
    changed = False
    for r in range(0, HEIGHT):
        temp_row = []
        for c in range(0, WIDTH):
            curr_val = grid[r][c]
            if curr_val == 'L':
                # check empty seat rule
                if get_pt2_occupied_seats(r, c) == 0:
                    curr_val = '#'
                    changed = True
            elif curr_val == '#':
                # check occupied seat rule
                if get_pt2_occupied_seats(r, c) >= 5:
                    curr_val = 'L'
                    changed = True
            temp_row.append(curr_val)
        temp_state.append(temp_row)

    # deep copy the temp_state grid
    grid = [[x for x in row] for row in temp_state]
    cycles += 1
    # print(f'[{cycles}]: Changed = {changed}')
    # print_grid(grid)

# we reached a stable state without any further changes
print(f'Part 2: Stable state reached after {cycles} cycles.')
# count occupied seats
occ_count = sum(1 for row in grid for seat in row if seat == '#')
print(f'Counted {occ_count} occupied seats.')

# Part 2: 1986 seats remain occupied
