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

def cut(inc, pos, size):
    # return (size - inc + pos) % size
    return (-inc + pos) % size

def deal_new(inc, pos, size):
    # return (size - pos - 1) % size
    return (-1 - pos) % size

def deal_inc(inc, pos, size):
    return (inc * pos) % size

def calc_pos(coeff, inc, pos, size):
    a, b = coeff
    return (a * inc + b * pos) % size

def shuffle2(stack, lines):
    for l in lines:
        if 'stack' in l:
            # reverse stack
            logging.debug(f'Dealing into new stack.')
            coeff = (-1, -1)
            inc = 1
            
        elif 'increment' in l:
            n = find_number(l)
            logging.debug(f'Increment: {n}.')
            coeff = (0, n)
            inc = 0
        elif 'cut' in l:
            n = find_number(l)
            logging.debug(f'Cut: {n}.')
            coeff = (-1, 1)
            inc = n

        new_stack = [-1] * size
        for i, c in enumerate(stack):
            new_stack[calc_pos(coeff, inc, i, size)] = c
        stack = new_stack[:]
        logging.debug(f'Stack: {stack}.')

    return stack

def shuffle(stack, lines):
    for l in lines:
        if 'stack' in l:
            # reverse stack
            logging.debug(f'Dealing into new stack.')
            stack = stack[::-1]
            logging.debug(f'Stack: {stack}.')
        elif 'increment' in l:
            n = find_number(l)
            logging.debug(f'Increment: {n}.')
            # Step through stack with increment
            new_stack = [-1] * size
            for i, c in enumerate(stack):
                new_stack[(i * n) % size] = c
            stack = new_stack[:]
            logging.debug(f'Stack: {stack}.')
        elif 'cut' in l:
            n = find_number(l)
            logging.debug(f'Cut: {n}.')
            stack = stack[n:] + stack[:n]
            logging.debug(f'Stack: {stack}.')

    return stack

#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    # part 1
    size = 10

    # part 2
    # size = 119315717514047

    f_name = 'example4.txt'

    stack = list(range(size))
    logging.debug(f'Current stack: {stack}')

    with open(f_name) as f:
        lines = f.readlines()

    stack_1 = stack[:]
    stack_1 = shuffle(stack, lines)
    stack_2 = stack[:]
    stack_2 = shuffle2(stack, lines)

    # Part 1
    # we are looking for the POSITION of card 2019, not the card at the 2019th position!
    # result_1 = stack.index(2019)
    # print(stack[result_1 - 5:result_1 + 5])
    # logging.info(f'Result 1 - card 2019 is at: {result_1}')

    # Part 2
    # logging.debug(f'At 2020: {stack[2020]}.')
