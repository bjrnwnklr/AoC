import re
import numpy as np
from collections import Counter

f_name = 'input.txt'

with open(f_name, 'r') as f:
    reg_num = r'([-]*\d+)'
    particles_array = [list(map(int, re.findall(reg_num, line.strip('\n')))) for line in f.readlines()]

# np.array of the particles
particles = np.array(particles_array)

# list contains number of particles per cycle
particles_per_cycle = []

cycles = 0
while cycles < 10000:
    alive = np.full(particles.shape[0], True)
    # calculate new position
    for i in range(3):
        # calculate new velocity
        particles[:, i+3] += particles[:, i+6]
        # calculate new position
        particles[:, i] += particles[:, i+3]

    # calculate collisions
    # - create normal array
    # - create tuples of position coordinates
    # - count occurences, using a Counter
    # - for every count > 1, remove all elements
    # - create new particles np.array
    part_list = particles.tolist()
    pos_tuples = list(map(tuple, particles[:, :3].tolist()))
    collisions = [item for item, count in Counter(pos_tuples).items() if count > 1]
    # find position of all matches
    for c in collisions:
        for i, p in enumerate(part_list):
            if tuple(p[:3]) == c:
                alive[i] = False

    particles = particles[alive]
    particles_per_cycle.append(particles.shape[0])
    cycles += 1

print(particles_per_cycle[-1])


# part 2: 574