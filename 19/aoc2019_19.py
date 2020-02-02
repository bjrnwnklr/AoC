# AOC 2019, day 19
import logging
from intcode import Intcode, InputInterrupt, OutputInterrupt
import numpy as np
import math


def print_grid(grid):
    for y in range(n_y):
        print(''.join(str(c) for c in grid[y]))


#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')


    # grid size
    n_x = 101
    n_y = 101

    

    raw_output = []
    grid = []

    # add input coordinates to int_comp.in_queue
    for y in range(n_y):
        for x in range(n_x):
            # initialize the intcode machine
            int_comp = Intcode(inp)
            int_comp.in_queue.append(x)
            int_comp.in_queue.append(y)

            # logging.debug(f'in_queue: {int_comp.in_queue}')

            while(not int_comp.done):
                try:
                    int_comp._run_intcode()
                except(InputInterrupt):
                    pass
                except(OutputInterrupt):
                    # collect all input, process later
                    raw_output.append(int_comp.out_queue.popleft())
                    # logging.debug(f'out_queue: {raw_output}')
                
        
    # print the grid
    for y in range(n_y):
        x_line = []
        for x in range(n_x):
            x_line.append(raw_output[n_y * y + x])
        grid.append(x_line)

    # print_grid(grid)

    logging.info(f'Result part 1: {sum(sum(x for x in line) for line in grid)} number of points affected.')

    # Part 1: 213

    ### part 2

    grid_array = np.array(grid)
    # empty array with square sums
    grid_square_sum = np.zeros(grid_array.shape)

    # Get the vector from 0,0 to left and right boundary in line 100
    y = 100
    left = np.min(np.argwhere(grid_array[y] == 1))
    right = np.max(np.argwhere(grid_array[y] == 1))
    logging.info(f'Row {y}: Left: {left}, Right: {right}')

    # in radians
    phi_left = np.arctan2(left, y)
    phi_right = np.arctan2(right, y)
    logging.info(f'Angles to y. Left: {phi_left}, right: {phi_right}')

    

    """
    # side length of square
    square = 4

    for y in range(n_y - square):
        for x in range(n_x - square):
            if grid_array[y, x] == 1:
                grid_square_sum[y, x] = np.sum(grid_array[y:y+square, x:x+square])


    # find the coordinates where the square fits in
    square_fits = np.argwhere(grid_square_sum == square ** 2)
    # logging.info(f'Square fits into the following coordinates: {square_fits}')

    # find closest coordinate
    dist = lambda x: math.sqrt(x[0] **2 + x[1]**2)
    nearest_square = np.apply_along_axis(dist, axis=1, arr=square_fits)
    # logging.info(f'Distance to emitter: {nearest_square}')

    result_2 = square_fits[np.argmin(nearest_square)]

    logging.info(f'Closest coordinates: {result_2}, answer = {result_2[0] + result_2[1] * 10000}')


    # print data for the 4 lines with smallest square
    for y in range(result_2[0], result_2[0] + square):
        line_left = np.min(np.argwhere(grid_array[y] == 1))
        line_right = np.max(np.argwhere(grid_array[y] == 1))
        logging.info(f'Row {y}: Left: {line_left}, Right: {line_right}')

        # calculate x coordinate for given y using x = tan(phi) * y
        x_left = np.around(np.tan(phi_left) * y)
        x_right = np.around(np.tan(phi_right) * y)
        logging.info(f'x for row {y}: left: {x_left}, right: {x_right}')
    """


