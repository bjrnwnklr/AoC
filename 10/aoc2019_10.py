# AOC 2019, day 10
import logging
from collections import defaultdict
import numpy as np

# get the unit vector for a given vector
def unit_vector(v):
    return v / np.linalg.norm(v)

def is_blocked(a, b, c):
    """
    Check if c blocks the line of sight between a and b.

    Calculates the vectors between a and b and a and c. Then checks if they have the same unit vector (same direction).
    If yes and a->c is shorter than a->b, c blocks a->b.
    """
    v_ab = np.array(a) - np.array(b)
    v_ac = np.array(a) - np.array(c)

    result = False

    # np.array_equal
    if np.allclose(unit_vector(v_ab), unit_vector(v_ac)):
        if np.linalg.norm(v_ac) < np.linalg.norm(v_ab):
            result = True

    return result  


def check_los(a, b, asteroids):
    to_check = [x for x in asteroids if x != a and x != b]
    return all(not is_blocked(a, b, c) for c in to_check)



#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    f_name = 'input.txt'


    with open(f_name) as f:
        asteroids = [(x, y) for y, l in enumerate(f) for x, c in enumerate(l) if c == '#']
        
    logging.debug('Asteroids: {} at {}'.format(len(asteroids), asteroids))

    seen = set()
    blocked = set()
    los = defaultdict(int)

    for a in asteroids:
        rest = [x for x in asteroids if x!= a]
        for b in rest:
            if (a, b) in seen or (b, a) in seen:
                los[a] += 1
            elif (a, b) in blocked or (b, a) in blocked:
                pass
            else:
                if check_los(a, b, asteroids):
                    los[a] += 1
                    seen.add((a, b))
                    seen.add((b, a))
                else:
                    blocked.add((a, b))
                    blocked.add((b, a))


    logging.debug('LOS counts: {}'.format(los))

    # get asteroid with highest line of sight count
    result = sorted(los, key=los.get, reverse=True)[0]

    logging.info('Part 1: {} asteroids can be seen from {}'.format(los[result], result))


# Part 1: 267 asteroids can be seen from (26, 28)