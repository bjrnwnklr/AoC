# Intcode virtual machine (as of AoC2019, day 15)

import logging
from intcode import Intcode, InputInterrupt, OutputInterrupt
from collections import defaultdict


# find all valid neighbors of a scaffolding element
def neighbors(grid, coord):

    # west, north, east, south
    _neighbor_pos = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    neighbor_coords = [(coord[0] + n[0], coord[1] + n[1]) for n in _neighbor_pos]
    valid_neighbors = [n for n in neighbor_coords if grid[n] == '#']
    return valid_neighbors


# finding intersections - check each grid entry that is a '#', then check if the neighbors (up, down, left, right) are '#'.
def find_intersections(grid):
    # find all entries with '#'
    scaffolding = [(x, y) for (x, y), c in grid.items() if c == '#']

    intersections = [c for c in scaffolding if len(neighbors(grid, c)) == 4]
    logging.debug('{} intersections found at {}'.format(len(intersections), intersections))
    return intersections

def robot_move(grid, robot, robot_dir):

    _step_count = 0
    _steps = []

    while(True):
        # get all valid neighbors for current position
        valid_neighbors = neighbors(grid, robot)

        possible_directions = [(robot[0] + robot_moves[robot_dir][i][0], robot[1] + robot_moves[robot_dir][i][1]) for i in range(3)]
        if possible_directions[0] in valid_neighbors:
            # we can still move ahead
            _step_count += 1
            # move robot one step ahead
            robot = possible_directions[0]
        elif possible_directions[1] in valid_neighbors:
            # we can turn left
            # store step_count and turn
            _steps.append(_step_count)
            _steps.append('L')
            # move robot position to the left
            robot = possible_directions[1]
            # turn robot to the left
            robot_dir = (robot_dir - 1) % 4
            # we have taken the first step already
            _step_count = 1
        elif possible_directions[2] in valid_neighbors:
            # we can turn right
            # store step_count and turn
            _steps.append(_step_count)
            _steps.append('R')
            # move robot position to the left
            robot = possible_directions[2]
            # turn robot to the left
            robot_dir = (robot_dir + 1) % 4
            # we have taken the first step already
            _step_count = 1
        else:
            # we have reached the end
            # record last step count
            _steps.append(_step_count)
            break

    return robot, robot_dir, _steps
    
# direction of robot
# North, West, South, East
directions = {'^': 0, '>': 1, 'v': 2, '<': 3}
# Ahead, left, right
robot_moves = [
    [(0, -1), (-1, 0), (1, 0)],
    [(1, 0), (0, -1), (0, 1)],
    [(0, 1), (1, 0), (-1, 0)],
    [(-1, 0), (0, 1), (0, -1)]
]

#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')

    # initialize the intcode machine
    int_comp = Intcode(inp)

    raw_output = []

    while(not int_comp.done):
        try:
            int_comp._run_intcode()
        except(InputInterrupt):
            pass
        except(OutputInterrupt):
            # collect all input, process later
            raw_output.append(int_comp.out_queue.popleft())
    
    # convert to characters
    char_output = [chr(x) for x in raw_output]

    with open('grid.txt', 'w') as f:
        f.write(''.join(str(x) for x in char_output))

    grid = defaultdict(int)
    x = y = 0
    for c in char_output:
        if c == '\n':
            y += 1
            x = 0
        else:
            grid[(x, y)] = c
            if c in ['^', 'v', '<', '>']:
                grid[(x, y)] = '#'
                robot = (x, y)
                robot_dir = directions[c]
            x += 1

    intersections = find_intersections(grid)

    part1 = sum(x * y for x, y in intersections)
    logging.info('Part 1: {}'.format(part1))

    logging.info('PART 1: End!')

    # part 1: 3608

    #### part 2

    # walk the scaffolding from start to finish, following this simple strategy:
    # - walk straight until we hit a wall 
    # - count number of steps
    # - turn left or right (there is always only one way)
    # - record turn
    # - repeat

    # we know where the robot is:
    start = robot
    robot, robot_dir, steps = robot_move(grid, robot, robot_dir)
    logging.info('Robot steps to reach end ({}, {}): {}'.format(robot, robot_dir, steps))

    for i in range(1, len(steps), 2):
        print('{}, {}'.format(steps[i], steps[i+1]))