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
    logging.basicConfig(level=logging.CRITICAL)

    logging.info('Starting up.')

    # read the bin file and convert it to a list of integers
    f_name = 'synacor/challenge.bin'
    int_data = syn_arch.read_bin(f_name)

    # create a VM
    vm = syn_arch.Synacor(int_data)

    # run the VM until we are done
    while(not vm.done):
        vm._run()

    print('Program ended.')