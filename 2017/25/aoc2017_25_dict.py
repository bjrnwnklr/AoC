from collections import defaultdict
import re

f_name = 'input.txt'

instructions = dict()

with open(f_name, 'r') as f:
    # read first two lines
    start_state = f.readline().strip('\n')[-2]
    diag_after = int(re.findall('(\d+)', f.readline().strip('\n'))[0])
    # read the rest and split into groups of instructions by state
    rest = f.read().strip('\n').split('\n\n')
    for state_instr in rest:
        # unpack the first line, the rest are in instr_lines
        state_line, *instr_lines = state_instr.split('\n')
        # state is 2nd to last element in the first line
        state = state_line.strip('\n')[-2]
        for i in (0, 4):
            curr_val = int(instr_lines[i].strip('\n')[-2])
            write_val = int(instr_lines[i+1].strip('\n')[-2])
            # find the direction by the 3rd to last character
            # 'f' in 'left', 'h' in 'right'
            # direction is used to rotate the deque
            # positive number: rotate to right, i.e. move to left
            # negative number: rotate to left, i.e. move to right
            direction = 1 if instr_lines[i+2].strip('\n')[-3] == 'f' else -1
            next_state = instr_lines[i+3].strip('\n')[-2]

            # create dictionary of instructions
            # key = state, current value
            # values = write which value, move into which direction, next state
            instructions[(state, curr_val)] = (write_val, direction, next_state)


# initialize the deque with 100 elements, all 0

tape = defaultdict(int)

curr_state = start_state
curr_pos = 0

for _ in range(diag_after):
    # read current tape value
    tape_val = tape[curr_pos]
    # get instructions (new state is automatically set)
    write_val, direction, curr_state = instructions[(curr_state, tape_val)]
    # write new value (in same place as popped off value)
    tape[curr_pos] = write_val
    # rotate tape 
    curr_pos += direction


# get checksum
checksum = sum(tape.values())
print(f'Checksum after {diag_after} cycles: {checksum}')

# Part 1: 2725