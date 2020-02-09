# Intcode virtual machine (as of AoC2019, day 15)

import logging
from intcode import Intcode, InputInterrupt, OutputInterrupt


def code_ascii(instr, reg1 = '', reg2 = ''):
    if not (reg1 and reg2):
        instructions = f'{instr}\n'
    else:
        instructions = f'{instr} {reg1} {reg2}\n'
    ascii_instructions = [ord(x) for x in instructions]

    logging.debug('Ascii instructions: {}'.format(ascii_instructions))

    return ascii_instructions

def decode_ascii(raw_output):
    return ''.join(chr(x) for x in raw_output)


    
#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')

    # initialize the intcode machine
    int_comp = Intcode(inp)

    # instructions are evaluated at each step

    #### PART 1 solution:
    # - jump if A is hole
    # - or jump if C is a hole
    # - but only if D is solid ground
    # ascii_instructions = [
    #     'NOT A J',
    #     'NOT C T',
    #     'OR T J',
    #     'AND D J',
    #     'WALK
    # ]
    
    #### PART 2 solution:
    ascii_instructions = [
        'OR  A T',
        'AND B T',
        'AND C T',
        'NOT T J',
        'OR  E T',
        'OR  H T',
        'AND T J',
        'AND D J',
        'RUN'
    ]

    # code up instructions into a list
    coded_instructions = [code_ascii(x) for x in ascii_instructions]

    # flatten the list
    flat_instructions = [x for l in coded_instructions for x in l]

    # feed the program into the intcode computer
    for x in flat_instructions:
        int_comp.in_queue.append(x) 

    while(not int_comp.done):
        try:
            int_comp._run_intcode()
        except(InputInterrupt):
            pass
        except(OutputInterrupt):
            # collect all input, process later
            c = int_comp.out_queue.popleft()
            if c < 400:
                print(decode_ascii([c]), end='')
            else:
                print('Result: ', c)

    
    
    logging.info('PART 1: End!')

