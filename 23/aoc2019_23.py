# Intcode virtual machine (as of AoC2019, day 15)

import logging
from intcode import Intcode, InputInterrupt, OutputInterrupt
from collections import defaultdict



    
#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')

    # start 50 intcode machines
    n = 50
    comps = []
    for i in range(n):
        # create a copy of the input program
        temp_inp = inp[:]
        # create intcode computer
        temp_comp = Intcode(temp_inp)
        # feed it the network address
        temp_comp.in_queue.append(i)
        # add to our list of computers
        comps.append(temp_comp)

    # dictionary with messages for each computer
    msg_queue = defaultdict(list)
    done = False
    i = 0

    # try this... run each intcode computer in turns?
    while not done:
        int_comp = comps[i]
        logging.debug(f'Comp {i}: checking msgs.')
        # check if we have a message for this computer?
        if msg_queue[i]:
            while msg_queue[i]:
                logging.debug(f'Comp {i}: message queue: {msg_queue[i]}.')
                # pop the leftmost message and feed it to the computer
                x, y = msg_queue[i].pop(0)
                int_comp.in_queue.append(x)
                int_comp.in_queue.append(y)
                logging.info(f'Comp {i} received msg ({x}, {y}).')

        output_counter = 0
        output_msg = []

        logging.debug(f'Comp {i}: running.')
        while(not int_comp.done):
            try:
                int_comp._run_intcode()
            except(InputInterrupt):
                int_comp.in_queue.append(-1)
                break
            except(OutputInterrupt):
                # collect all input, process later
                c = int_comp.out_queue.popleft()
                output_msg.append(c)
                if output_counter == 2:
                    # we got a complete message, so add it to the msg_queue
                    address, x, y = output_msg
                    # check if we found the message addressed to 255:
                    if address == 255:
                        logging.info(f'Comp {i}: Message to 255 received: ({x}, {y})')
                        done = True
                    msg_queue[address].append((x, y))
                    logging.info(f'Comp {i}: sending msg to comp {address}: ({x}, {y})')
                    output_counter = 0
                    break
                else:
                    output_counter += 1


        # next computer
        i = (i + 1) % n
    
    
    logging.info('PART 1: End!')

    # part 1 answer: 24106

