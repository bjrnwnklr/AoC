# Synacor main program

from collections import defaultdict
import logging
import numpy as np
import sys

import syn_arch


######
#
# Main program
# 
if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    logging.info('Starting up.')

    # try reading the bin file
    f_name = 'challenge.bin'

    int_data = syn_arch.read_bin(f_name)

    vm = syn_arch.Synacor(int_data)

    while(not vm.done):
        vm._run()