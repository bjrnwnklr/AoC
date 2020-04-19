# AOC 2019, day 16
import logging

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
        pattern.append(line)

    return pattern

def calc_output_position(input_number, pattern):
    pat_length = len(pattern)

    output_full_number = sum(x * pattern[i % pat_length] for i, x in enumerate(input_number, start=1))
    output = list(map(int, list(str(abs(output_full_number)))))[-1]
    logging.debug('Output generated for {} and pattern {}: {} (full sum: {})'.format(input_number, pattern, output, output_full_number))
    return output


#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    f_name = 'ex1.txt'

    with open(f_name) as f:
        inp = [int(x) for x in list(f.readline().strip('\n'))]

    # inp = inp[:8]

    pattern = create_pattern(len(inp))

    next_number = inp[:]

    for _ in range(4):
        next_number = [calc_output_position(next_number, p) for p in pattern]

        logging.debug('New number: {}'.format(next_number))

    part1 = ''.join([str(x) for x in next_number])

    logging.info('Part 1: {}'.format(part1))
    logging.info('First 8 digits: {}'.format(part1[:8]))