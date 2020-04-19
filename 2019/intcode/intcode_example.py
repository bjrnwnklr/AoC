# Intcode virtual machine (as of AoC2019, day 15)

import logging
from intcode import Intcode

    
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

    
    # Do something with the intcode, typically running input / output loops. 
    input_signal = 0
    output = int_comp.run_input_output(input_signal)

    # take a copy of the intcode machine and store it somewhere
    int_comp_copy = int_comp.clone()
    
    logging.info('PART 1: End!')

