# AOC 2019, day 22
import logging
import re

# example 1: Result: 0 3 6 9 2 5 8 1 4 7
# example 2: Result: 3 0 7 4 1 8 5 2 9 6
# example 3: Result: 6 3 0 7 4 1 8 5 2 9
# example 4: Result: 9 2 5 8 1 4 7 0 3 6


def find_number(line):
    number = list(map(int, re.findall(r'-?\d+', line)))[0]
    return number

def shuffle(stack, lines):
    for l in lines:
        if 'stack' in l:
            # reverse stack
            stack = stack[::-1]
        elif 'increment' in l:
            n = find_number(l)
            # Step through stack with increment
            new_stack = [-1] * size
            for i, c in enumerate(stack):
                new_stack[(i * n) % size] = c
            stack = new_stack[:]
        elif 'cut' in l:
            n = find_number(l)
            stack = stack[n:] + stack[:n]

    return stack

#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    # part 1
    # size = 10007

    # part 2
    size = 119315717514047

    f_name = 'input.txt'

    stack = list(range(size))
    # logging.debug(f'Current stack: {stack}')

    with open(f_name) as f:
        lines = f.readlines()

    
    stack = shuffle(stack, lines)

    # Part 1
    # we are looking for the POSITION of card 2019, not the card at the 2019th position!
    # result_1 = stack.index(2019)
    # print(stack[result_1 - 5:result_1 + 5])
    # logging.info(f'Result 1 - card 2019 is at: {result_1}')

    # Part 2
    logging.debug(f'At 2020: {stack[2020]}.')
