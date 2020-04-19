# Intcode virtual machine (as of AoC2019, day 15)

import logging
from intcode import Intcode, InputInterrupt, OutputInterrupt
from collections import defaultdict
from itertools import combinations

def code_ascii(instr):
    instructions = f'{instr}\n'
    ascii_instructions = [ord(x) for x in instructions]

    logging.debug('Ascii instructions: {}'.format(ascii_instructions))

    return ascii_instructions

def decode_ascii(raw_output):
    return ''.join(chr(x) for x in raw_output)

def get_input():
    return input('Please enter command: ')

def get_item_combs(items):
    all_combs = []
    for n in range(len(items) + 1):
        all_combs.extend(list(combinations(items, n)))
    return all_combs

#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')


    
    # define / update instructions here!
    base_instructions = [
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

    # create set of all items we can pickup
    items = {
        'antenna',
        'weather machine',
        'klein bottle',
        'spool of cat6',
        'mug',
        'cake',
        'tambourine',
        'shell'
    }

   
    

    # now create a generator with all combinations
    item_combs = get_item_combs(items)

    for z, curr_items in enumerate(item_combs):
        # start up the intcode computer
        print(f'{z} - Starting with items: {curr_items}')
        int_comp = Intcode(inp[:])
        output_buffer = ''
        instructions = base_instructions[:]

        while(not int_comp.done):
            try:
                int_comp._run_intcode()
            except(InputInterrupt):
                # check if there are any instructions in the queue - if yes, pop the first and process
                if instructions:
                    ascii_cmd = code_ascii(instructions.pop(0))
                    int_comp.in_queue.extend(ascii_cmd)


                else:
                    ### Build code here where we try different iterations of the items
                    # determine all items we need to drop
                    items_to_drop = items - set(curr_items)
                    # print(f'dropping: {items_to_drop}')
                    for i in items_to_drop:
                        instructions.append(f'drop {i}')
                    instructions.append('east')


            except(OutputInterrupt):
                # collect all input, process later
                c = int_comp.out_queue.popleft()
                output_buffer += chr(c)
                if output_buffer[-9:] == 'Command?\n':
                    # check if we got ejected from the security barrier
                    if 'Analyzing' in output_buffer:
                        if 'ejected' in output_buffer:
                            weight = 'heavier' if 'heavier' in output_buffer else 'lighter'
                            print(f'{z} - Ejected ({weight}). Items: {curr_items}')
                            # print(output_buffer)
                        else:
                            print(f'List of current items: {curr_items}')
                            print(output_buffer)
                        break
                    # flush output_buffer
                    output_buffer = ''
    
    logging.info('PART 1: End!')
