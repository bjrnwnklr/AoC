""" 
Run the intcode easter egg program hidden in the 2021 Day 7 input.

Output produced are Unicode codes which translate to:
`Ceci n'est pas une intcode program\n`

Run this program from the `2021` folder with `python -m solutions.intcode_202107`

"""

# Intcode virtual machine (as of AoC2019, day 15)

import logging
from .intcode import Intcode, InputInterrupt, OutputInterrupt


#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    # read input
    f_name = 'input/07.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')

    # initialize the intcode machine
    int_comp = Intcode(inp)
    output_msg = []

    while(not int_comp.done):
        try:
            int_comp._run_intcode()
        except(OutputInterrupt):
            # collect all input, process later
            c = int_comp.out_queue.popleft()
            output_msg.append(c)

    print(
        ''.join(chr(c) for c in output_msg)
    )

    logging.info('PART 1: End!')
