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

        # flatten the array of arrays
        line = list(np.ravel(line))

        # if pattern is not long enough, extend it until it's longer than n.
        if len(line) < n + 1:
            line = [line] * ((n // len(line)) + 1)
            line = list(np.ravel(line))

        pattern.append(line[1:n+1])

    return np.array(pattern)


#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    f_name = 'input.txt'

    with open(f_name) as f:
        inp = [int(x) for x in list(f.readline().strip('\n'))]


    pattern = create_pattern(len(inp))
    next_number = np.array(inp)

    for _ in range(100):
        # simply take the dot product between our pattern matrix and the input number to generate the next number
        # then mod the absolute number by 10 to get the last digit.
        next_number = pattern.dot(next_number)
        next_number = np.mod(np.abs(next_number), 10)


    part1 = ''.join([str(x) for x in next_number])

    logging.debug('Part 1: {}'.format(part1))
    logging.info('First 8 digits: {}'.format(part1[:8]))

# part 1: 19944447


    ######## part 2

    repeats = 10000

    # find length of number required
    offset = int(''.join([str(x) for x in inp[:7]]))
    logging.debug('Offset for part 2: {}'.format(offset))
    input_length = len(inp) * repeats
    logging.debug('Length of input after {} repeats: {}'.format(repeats, input_length))
    remaining_length = input_length - offset
    logging.debug('Remaining length: {}'.format(remaining_length))

    # take the input from the offset on
    pt2_input = inp * repeats
    next_number = np.array(pt2_input[offset:])
    # next_number = pt2_input[offset:]
    logging.debug('Part 2 input length: {}'.format(len(next_number)))

    # sum up from the back (starting with last element)
    for j in range(100):
        ## This is a slightly slower version not using numpy, updating the same list 
        # (uncomment the line above with the next_number definition)
        #
        # for i in range(len(next_number) - 1, 0, -1):
        #     next_number[i-1] = (next_number[i-1] + next_number[i]) % 10

        next_number = np.mod(np.cumsum(next_number[::-1]), 10)
        next_number = next_number[::-1]

        logging.debug('{}'.format(j))


    part2 = ''.join([str(x) for x in next_number[:8]])
    logging.info('Part 2: {}'.format(part2))
    
