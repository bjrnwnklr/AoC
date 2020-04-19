# AOC 2019, day 12
import logging
import re
from itertools import combinations


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
            



#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    f_name = 'input.txt'
    input_file = open(f_name, 'r')
    raw_pos = [[*map(int, re.findall(r'-?\d+', l))] for l in input_file.readlines() if l]

    logging.debug('{}'.format(raw_pos))

    moons = [Moon(i, *p) for i, p in enumerate(raw_pos)]

    for m in moons:
        logging.debug('{}'.format(m))


    # time epoch - start at 0
    epochs = 1000
    for t in range(1, epochs + 1):

        # get pairs of moons - use combinations
        # apply gravity to each pair of moons
        for a, b in combinations(moons, 2):
            apply_gravity(a, b)

        # apply velocity to each moon
        for m in moons:
            m.apply_velocity()


        logging.debug('Time: after {} steps.'.format(t))
        for m in moons:
            logging.debug('{}'.format(m))

    # calculate total energy in system
    tot_energ = sum(m.total_energy() for m in moons)

    logging.info('Total energy after {} steps: {}'.format(epochs, tot_energ))

    # Part 1: 8044
    