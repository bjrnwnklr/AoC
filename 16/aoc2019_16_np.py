# AOC 2019, day 16
import logging
import numpy as np

"""
- read in number and split into a list of digits
- construct repeating pattern:
  - base pattern is 0, 1, 0, -1
  - repeat each value in pattern equal to position in output list (e.g. for 2nd digit of the output, repeat each pattern element 2 times)
  - skip the first value of the pattern exactly once
- multiply elements and add up
- take only the last digit as new output value
"""

def create_pattern(n):
    base = [0, 1, 0, -1]

    pattern = []

    for i in range(1, n + 1):
        line = [[x] * i for x in base]

        line = [x for l in line for x in l]
        if len(line) < n + 1:
            line = [line] * ((n // len(line)) + 1)
            line = [x for l in line for x in l]
        pattern.append(line[1:n+1])

    return np.array(pattern)


#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    f_name = 'input.txt'

    with open(f_name) as f:
        inp = [int(x) for x in list(f.readline().strip('\n'))]

    # inp = inp[:8]

    pattern = create_pattern(len(inp))
    next_number = np.array(inp)

    for _ in range(100):
        next_number = pattern.dot(next_number)
        next_number = np.mod(np.abs(next_number), 10)


    part1 = ''.join([str(x) for x in next_number])

    logging.info('Part 1: {}'.format(part1))
    logging.info('First 8 digits: {}'.format(part1[:8]))

# part 1: 19944447