import re
import numpy as np
from collections import Counter

f_name = 'input.txt'

with open(f_name, 'r') as f:
    reg_num = r'([-]*\d+)'
    particles_array = [list(map(int, re.findall(reg_num, line.strip('\n')))) for line in f.readlines()]

particles = np.array(particles_array)
closest_per_cycle = []

cycles = 0
while cycles < 10000:

    # calculate new position
    for i in range(3):
        # calculate new velocity
        particles[:, i+3] += particles[:, i+6]
        # calculate new position
        particles[:, i] += particles[:, i+3]

    # calculate distance
    dist = np.sum(np.absolute(particles[:, :3]), axis=1)

    # closest particle
    p_closest = np.argmin(dist)
    p_lowest_dist = dist[p_closest]
    closest_per_cycle.append((p_closest, p_lowest_dist))

    cycles += 1

counter = Counter([c[0] for c in closest_per_cycle])

print(counter.most_common(10))

# part 1: 376
