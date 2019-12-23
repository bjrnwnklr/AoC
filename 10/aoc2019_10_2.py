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


    # our new starting position is at (26, 28) - for real puzzle
    # for example 2 (largest), it is at (11, 13)
    station = (26, 28)
    #station = (11, 13)

    # Remove station from list of asteroids first...
    asteroids.remove(station)
    
    # create np array of relative coordinates (reverse y coordinate to align to cartesian coordinates)
    asts_rel = np.array(asteroids) - np.array(station)
    asts_rel[:, 1] *= -1

    # create np array of length of vectors from station to each asteroid
    asts_dist = np.linalg.norm(asts_rel, axis=1)

    # create np array of angle to the "up" vector using np.arctan2(y, x)
    asts_angle = np.arctan2(asts_rel[:, 0], asts_rel[:, 1]) * 180 / np.pi
    # convert quadrants (e.g. -90) into full polar coordinates (e.g. 270)
    asts_angle = (asts_angle + 360) % 360

    # create a dictionary of angles with a list of asteroids at the angle / distance tuples
    a_tups = defaultdict(list)
    for ang, coord in zip(list(asts_angle), [(x, y) for x, y in asts_rel]):
        a_tups[ang].append(coord)

    # dictionary of distances for quick lookup
    dists = dict(zip([(x, y) for x, y in asts_rel], list(asts_dist)))
    
    # create a list of unique angles and sort ascending (use a set to create unique list)
    # use a deque so we can pop off and append angles
    angles = deque(sorted(set(asts_angle)))

    # dictionary of destroyed asteroids
    destroyed = dict()
    # counter of destroyed asteroids
    counter = 0

    # rotate through the angles and see what we have matching
    while angles:
        # get next angle
        curr = angles[0]

        # find all asteroids on the same vector
        same_v = a_tups[curr]

        if same_v:
            # sort by distance and get the closest one
            same_sorted = sorted(same_v, key=lambda x: dists[x])
            closest = same_sorted[0]

            # destroy the asteroid
            counter += 1
            # save destroyed asteroid and add the station address again
            abs_coord = (closest[0] + station[0], closest[1] * -1 + station[1])
            destroyed[counter] = abs_coord
            a_tups[curr].remove(closest)

            logging.debug('Destroyed asteroid # {}: {}'.format(counter, destroyed[counter]))

            # move angles to the next angle
            angles.rotate(-1)
        else:
            # no further asteroid found under this angle, so remove it
            angles.popleft()

twohundred = destroyed[200]
logging.info('Part 2: {} (200th asteroid: {})'.format(twohundred[0] * 100 + twohundred[1], twohundred))

# Part 1: 267 asteroids can be seen from (26, 28)