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
    return input('Please enter command: ')
    
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

    
    # define / update instructions here!
    instructions = [
        'east',
        'take antenna',
        'west',
        'north',
        'take weather machine',
        'north',
        'take klein bottle',
        'east',
        'take spool of cat6',
        'east',
        'south',
        'take mug',
        'north',
        'north',
        'west',
        'north',
        'take cake',
        'south',
        'east',
        'east',
        'north',
        'north',
        'take tambourine',
        'south',
        'south',
        'south',
        'take shell',
        'north',
        'west',
        'south',
        'west',
        'south',
        'south',
    ]

    items = [
        'antenna',
        'weather machine',
        'klein bottle',
        'spool of cat6',
        'mug',
        'cake',
        'tambourine',
        'shell'
    ]


    while(not int_comp.done):
        try:
            int_comp._run_intcode()
        except(InputInterrupt):
            # check if there are any instructions in the queue - if yes, pop the first and process
            if instructions:
                ascii_cmd = code_ascii(instructions.pop(0))
            else:
                cmd = get_input()
                if cmd == 'exit':
                    break
                ascii_cmd = code_ascii(cmd)

            int_comp.in_queue.extend(ascii_cmd)
        except(OutputInterrupt):
            # collect all input, process later
            c = int_comp.out_queue.popleft()
            print(decode_ascii([c]), end='')

    
    logging.info('PART 1: End!')
