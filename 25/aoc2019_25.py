# Intcode virtual machine (as of AoC2019, day 15)

import logging
from intcode import Intcode, InputInterrupt, OutputInterrupt
from collections import defaultdict

def code_ascii(instr):
    instructions = f'{instr}\n'
    ascii_instructions = [ord(x) for x in instructions]

    logging.debug('Ascii instructions: {}'.format(ascii_instructions))

    return ascii_instructions

def decode_ascii(raw_output):
    return ''.join(chr(x) for x in raw_output)

def get_input():
    cmd = input('Please enter command:')
    return code_ascii(cmd)
    
#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')

    # start up the intcode computer
    int_comp = Intcode(inp)

    """
    # define / update instructions here!
    instructions = [
        'east'
    ]

    # code up each set of instructions
    coded_instructions = [code_ascii(instr) for instr in instructions]
    # flatten the list into one list of ascii instructions
    flat_instructions = [x for l in coded_instructions for x in l]

    # feed the flat list of instructions into the intcode computer
    for x in flat_instructions:
        int_comp.in_queue.append(x) 

    """

    while(not int_comp.done):
        try:
            int_comp._run_intcode()
        except(InputInterrupt):
            ascii_cmd = get_input()
            int_comp.in_queue.extend(ascii_cmd)
        except(OutputInterrupt):
            # collect all input, process later
            c = int_comp.out_queue.popleft()
            print(decode_ascii([c]), end='')

    
    logging.info('PART 1: End!')
