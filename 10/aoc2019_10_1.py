# AOC 2019, day 10
import logging
from collections import defaultdict, deque
import numpy as np

#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    f_name = 'input.txt'


    with open(f_name) as f:
        asteroids = [(x, y) for y, l in enumerate(f) for x, c in enumerate(l) if c == '#']
        
    logging.debug('Asteroids: {} at {}'.format(len(asteroids), asteroids))

    los_dict = dict()

    for a in asteroids:
        rest = [x for x in asteroids if x != a]
        
        # create np array of relative coordinates (reverse y coordinate to align to cartesian coordinates)
        asts_rel = np.array(rest) - np.array(a)
        
        # create np array of angle to the 'right'vector using np.arctan2(y, x)
        asts_angle = np.arctan2(asts_rel[:, 1], asts_rel[:, 0]) * 180 / np.pi
        
        # create a set of unique angles
        angles = set(asts_angle)

        los_dict[a] = len(angles)

    # get asteroid with highest number of line of sight
    result = sorted(los_dict, key=los_dict.get, reverse=True)[0]

    logging.info('Part 1: {} asteroids can be seen from {}'.format(los_dict[result], result))


# Part 1: 267 asteroids can be seen from (26, 28)
# Part 2: 1309 (200th asteroid: (13, 9))