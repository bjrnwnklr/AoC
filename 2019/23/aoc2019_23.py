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

    # Initialize the nat memory as a tuple
    nat_mem = (-1, -1)
    nat_y = [0]
    # all computers are considered to be idle from the start
    # we can then check if the sum of the values of the idle dict == n 
    # - meaning all computers have been idle
    idle_dict = {i: False for i in range(n)}

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
                idle_dict[i] = True
                break
            except(OutputInterrupt):
                # collect all input, process later
                c = int_comp.out_queue.popleft()
                output_msg.append(c)
                idle_dict[i] = False
                if output_counter == 2:
                    # we got a complete message, so add it to the msg_queue
                    address, x, y = output_msg
                    # check if we found the message addressed to 255:
                    if address == 255:
                        logging.info(f'Comp {i}: Message to 255 received: ({x}, {y})')
                        # store nat values - we don't need to check here if two received in a row!
                        nat_mem = (x, y)
                    msg_queue[address].append((x, y))
                    logging.info(f'Comp {i}: sending msg to comp {address}: ({x}, {y})')
                    output_counter = 0
                    break
                else:
                    output_counter += 1


        # next computer
        i = (i + 1) % n
        if i == 0:
            idle_count = sum(idle_dict.values())
            # check if all computers have been idle
            if idle_count == n:
                logging.info(f'Comp {i}: Network idle detected. Idle count = {idle_count}.')
                # send nat_mem to computer 0
                x, y = nat_mem
                comps[0].in_queue.append(x)
                comps[0].in_queue.append(y)

                # check y values for messages sent to computer 0
                if nat_y[-1] == y:
                    logging.info(f'Comp {i}: Same y value detected: {y}. Stopping!')
                    done = True
                else:
                    nat_y.append(y)
    
    
    logging.info('PART 1: End!')

    # part 1 answer: 24106
    # part 2 answer: 17895

