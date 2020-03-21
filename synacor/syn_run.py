# Synacor main program

from collections import defaultdict
import logging
import numpy as np
import sys
import argparse
import pickle

import syn_arch


######
#
# Main program
# 
if __name__ == '__main__':
    # set logging level
    # logging.basicConfig(level=logging.DEBUG, filename='sys_debug.log')
    logging.basicConfig(level=logging.CRITICAL)

    # parse command line arguments. 
    # -l / --load argument: load a VM state from a pickle file
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--load', help='Load Synacor VM from saved .pickle file.')
    
    args = parser.parse_args()

    if args.load:
        # if a file was passed in, open it and load the VM from it
        f_name = args.load
        logging.info(f'Loading VM from file "{f_name}".')

        with open(f_name, 'rb') as f:
            vm = pickle.load(f)

    else:
        # no pickle file specified, start a fresh new VM
        logging.info('Starting fresh new VM.')
        # read the bin file and convert it to a list of integers
        f_name = 'challenge.bin'
        int_data = syn_arch.read_bin(f_name)
        # create a new VM from the standard challenge file
        vm = syn_arch.Synacor(int_data)

    # run the VM until we are done
    while(not vm.done):
        vm._run()

    print('Program ended.')