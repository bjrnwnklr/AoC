# Synacor main program

from collections import defaultdict
import logging

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

    with open(f_name, 'rb') as f:
        data = f.read()

        print(data)