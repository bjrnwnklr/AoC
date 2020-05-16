import numpy as np


def to_np_array(instr):
    return np.array([[c == '#' for c in row] for row in instr.split('/')])

grid = np.array([[False, True, False], [False, False, True], [True, True, True]])

f_name = 'input.txt'
rules = dict()


with open(f_name, 'r') as f:
    for line in f.readlines():
        # convert left and right side of rules to np.array
        left, right = map(to_np_array, line.strip('\n').strip().split(' => '))
        # now calculate all combinations of flip and rotating
        for pat in [left, np.fliplr(left)]:
            for i in range(4):
                rules[np.rot90(pat, i).tobytes()] = right

print(f'Rules: {len(rules)}')

# rules now contains all possible patterns and their enhancement output
cycles = 18

for cycle in range(cycles):
    # check if divisible by 2
    if grid.shape[0] % 2 == 0:
        square_size = 2
    else:
        square_size = 3



    # break into square_size grids
    num_squares = grid.shape[0] // square_size
    new_grid = []
    for r in range(num_squares):
        temp_row = []
        for c in range(num_squares):
            # get the cell we want to transform
            temp_cell = grid[square_size*r:square_size*r+square_size,square_size*c:square_size*c+square_size]
            # do the transformation
            # get the transformation value and append it to the temporary row
            temp_row.append(rules[temp_cell.tobytes()])
        new_grid.append(np.concatenate(temp_row, axis=1))

    grid = np.concatenate(new_grid, axis=0)
    print(grid.shape)

    # count number of pixels in grid
    print(f'Cycle: {cycle}. Number of pixels: {np.sum(grid)}')
    
    # Part 1: 155
    # Part 2: 2449665
