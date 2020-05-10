import re
import numpy as np
from collections import Counter

f_name = 'ex2.txt'

with open(f_name, 'r') as f:
    reg_num = r'([-]*\d+)'
    particles_array = [list(map(int, re.findall(reg_num, line.strip('\n')))) for line in f.readlines()]

# np.array of the particles
particles = np.array(particles_array)
# status of particles (True = alive, False = destroyed)
alive = np.full(particles.shape[0], True)
# list of closest particle per cycle
closest_per_cycle = []

cycles = 0
while cycles < 100:

    # calculate new position
    for i in range(3):
        # calculate new velocity
        particles[:, i+3] += particles[:, i+6]
        # calculate new position
        particles[:, i] += particles[:, i+3]

    # calculate collisions
    for i, p in enumerate(particles):
        alive


    cycles += 1

print(f'Particles left: {particles.shape[0]}')

