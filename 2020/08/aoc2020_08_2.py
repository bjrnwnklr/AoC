import logging
from gameconsole import *


def check_instr(raw_mem, locations, change_from='nop', change_to='jmp'):
    # now iterate through all NOP instances and change to JMP, then run a program
    temp_locs = locations[:]
    done = False
    while (not done) and temp_locs:
        # create a copy of the raw_mem program
        temp_prgm = raw_mem[:]
        # get the next location of the nop/jmp instruction and change it
        next_op = temp_locs.pop()
        instr_to_change = temp_prgm[next_op]
        new_instr = instr_to_change.replace(change_from, change_to)
        temp_prgm[next_op] = new_instr

        # now run the emulation and check if we have a successful termination
        gc_instance = GameConsole(temp_prgm)
        status = gc_instance.run()
        if status == GC_TERMINATED:
            done = True
            print(f'Program cleanly terminated. Change instruction at line [{next_op}] from {change_from} to {change_to}')


if __name__ == '__main__':
    # set logging level
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)

    # read in input
    f_name = 'input.txt'
    raw_mem = []

    # build an emulator that first tries replacing one NOP for a JMP, then replace each JMP for NOP

    # first, read in the program
    with open(f_name, 'r') as f:
        for line in f.readlines():
            raw_mem.append(line.strip('\n'))

    # find all NOP and JMP lines
    nops = [i for i, l in enumerate(raw_mem) if 'nop' in l]
    jmps = [i for i, l in enumerate(raw_mem) if 'jmp' in l]

    check_instr(raw_mem, nops, 'nop', 'jmp')
    check_instr(raw_mem, jmps, 'jmp', 'nop')

# Part 2: 780 (change line 265 from jmp to nop)