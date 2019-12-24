# AOC 2019, day 12
import logging
import re
from itertools import combinations
import math


class Moon():

    def __init__(self, n, x, y, z):
        self.pos = (x, y, z)
        self.vel = (0, 0, 0)
        self.n = n
        
    def __str__(self):
        return('n: {}, pos: {}, vel: {}'.format(self.n, self.pos, self.vel))

    def apply_velocity(self):
        self.pos = tuple(self.pos[i] + self.vel[i] for i in range(3))

        
    def total_energy(self):
        # potential energy
        pot = sum(abs(x) for x in self.pos)
        # kinetic energy
        kin = sum(abs(x) for x in self.vel)

        return pot * kin


def apply_gravity(a, b):
    delta_a = []
    delta_b = []

    for i in range(3):
        a_c = a.pos[i]
        b_c = b.pos[i]
        if a_c == b_c:
            a_t = 0
            b_t = 0
        elif a_c < b_c:
            a_t = 1
            b_t = -1
        elif a_c > b_c:
            a_t = -1
            b_t = 1

        delta_a.append(a_t)
        delta_b.append(b_t)

    # update velocity
    a.vel = tuple(a.vel[i] + delta_a[i] for i in range(3))
    b.vel = tuple(b.vel[i] + delta_b[i] for i in range(3))

def _lcm(a, b):
    return a * b // math.gcd(a, b)

#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    f_name = 'input.txt'
    input_file = open(f_name, 'r')
    raw_pos = [[*map(int, re.findall(r'-?\d+', l))] for l in input_file.readlines() if l]

    # create moons
    moons = [Moon(i, *p) for i, p in enumerate(raw_pos)]

    start_pos = [tuple([m.pos[i] for m in moons]) for i in range(3)]
    start_vel = [tuple([m.vel[i] for m in moons]) for i in range(3)]

    freq = [set() for i in range(3)]

    # time epoch - start at 0
    epochs = 500000
    for t in range(1, epochs + 1):

        # get pairs of moons - use combinations
        # apply gravity to each pair of moons
        for a, b in combinations(moons, 2):
            apply_gravity(a, b)

        # apply velocity to each moon
        for m in moons:
            m.apply_velocity()

        # check for frequencies for each dimension
        # check if in previous configuration - for each dimension
        for i in range(3):
            pos = tuple([m.pos[i] for m in moons])
            vel = tuple([m.vel[i] for m in moons])
            if (pos, vel) == (start_pos[i], start_vel[i]):
                
                # store frequency of repeated position
                freq[i].add(t)


    min_freqs = [min(freq[i]) for i in range(3)]

    result = _lcm(_lcm(min_freqs[0], min_freqs[1]), min_freqs[2])

    logging.info('LCM of frequencies: {}'.format(result))



    # Part 1: 8044
    # Part 2: 362375881472136
    