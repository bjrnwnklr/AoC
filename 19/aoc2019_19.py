# AOC 2019, day 19
import logging
from intcode import Intcode, InputInterrupt, OutputInterrupt
import numpy as np
import math


def print_grid(grid):
    for y in range(n_y):
        print(''.join(str(c) for c in grid[y]))


def in_beam(inp, y, x):
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
            output = int_comp.out_queue.popleft()

    return output

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


    # run intcode from line 100 on and check if we found a square match
    square = 99

    start_y = 100
    end_y = 1100
    start_x = 0

    x = start_x
    x_beam = 0
    for y in range(start_y, end_y):
        left_not_found = True

        while left_not_found:
            c = in_beam(inp, y, x)
            # logging.info(f'Checking y: {y}, x: {x}. Result: {c}')
            if c:
                left_not_found = False
                x_beam = x
                # check top right corner
                top_right = in_beam(inp, y - square, x + square)
                if top_right:
                    # we found a square that fits!
                    logging.info(f'Found square!!! y: {y - square}, x: {x_beam}')
                else:
                    pass
                    # logging.info(f'No square at y: {y - square}, x: {x_beam}')
            else:
                x += 1

        x = x_beam - 3
        

    # part 2 solved!!!! y = 987, x = 783, result = 7830987

    """
    grid_array = np.array(grid)
    grid_square_sum = np.zeros(grid_array.shape)

    # Get the vector from 0,0 to left and right boundary in line 100
    y = 100
    left = np.min(np.argwhere(grid_array[y] == 1))
    right = np.max(np.argwhere(grid_array[y] == 1))
    logging.info(f'Row {y}: Left: {left}, Right: {right}')

    # calculate angle from -y axis to beam in radians
    phi_left = np.arctan2(left, y)
    phi_right = np.arctan2(right, y)
    logging.info(f'Angles to y. Left: {phi_left}, right: {phi_right}')

    # solution using numpy

    # side length of square
    square = 100

    # y length to try
    y_max = 10000

    # calculate np.arrays with the coordinates for each y value
    # start from height of square
    bottom_left_y = np.arange(square - 1, y_max)
    bottom_left_x = np.around(np.tan(phi_left) * bottom_left_y)
    bottom_right_x = np.around(np.tan(phi_right) * bottom_left_y)



    # calculate the top right values, this time starting from 0
    top_right_y = np.arange(y_max - square + 1)
    top_right_x = np.around(np.tan(phi_right) * top_right_y)
    # top_right_x = np.around(np.tan(phi_right) * bottom_left_y)

    # now find all values where x_right - x_left >= square
    dx = (top_right_x - bottom_left_x) >= (square - 1)
    min_top_right_x = np.min(np.argwhere(dx == True))
    min_top_left_y = np.argwhere(top_right_x == min_top_right_x)

    part_2_coords = (int(min_top_left_y), int(bottom_left_x[min_top_left_y]))

    logging.debug(f'dx: {np.sum(dx)}')
    logging.debug(f'Smallest top right x: {min_top_right_x} at y pos: {min_top_left_y}')
    logging.info(f'top left corner of square: {part_2_coords}, answer = {part_2_coords[0] + part_2_coords[1] * 10000}')

    # Wrong answer: INFO:root:top left corner of square: (1198, 947), answer = 9471198 (too high!)

    # generate segments for lines 1100 to 1400
    test_y = np.arange(1000, 1300)
    test_left_x = np.around(np.tan(phi_left) * test_y)
    test_right_x = np.around(np.tan(phi_right) * test_y)

    for i in range(len(test_y)):
        print(f'y: {test_y[i]} l: {test_left_x[i]} r: {test_right_x[i]}')

    print('----\n')
    for i in range(100, len(test_y)):
        print(f'y: {test_y[i]} t_r - b_l: {test_right_x[i - 99] - test_left_x[i]}')

    
    for y in range(square - 1, 45):
        logging.debug(f'y: {y}, bottom_left_x: {bottom_left_x[y]}, top_right_x: {top_right_x[y]}')

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


