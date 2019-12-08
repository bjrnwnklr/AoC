# Using intcode...

### Part 1

# will require some modifications:
# 1) start 5 runs of the code in sequence (should be easy!)
# 2) provide automated input to the 'input' function 
# - need to provide two different inputs:
#   a) phase (0-5)
#   b) output from previous run
# - use a stack to provide input (one stack for all programs)
# - first push all phases onto stack
# - pop first phase
# - push output from 1 onto 2nd position of stack
# etc
# 3) modify the output function so that it prints / stores the output
# 4) keep a list of all results and the phase input

from itertools import permutations

def get_param(param_count, ip, param, mem):
    mems = []
    # go through each parameter and retrieve value based on parameter mode
    for i in range(1, param_count + 1):
        p_mode = int(param[-i]) # -i since param mode goes from right to left
        if p_mode == 1:         # immediate mode
            m = mem[ip + i]
        else:                   # position mode
            m = mem[mem[ip + i]]
        mems.append(m)

    return mems

### OP CODE = 1
# ADD
def add(ip, param, mem, *args):
    param_count = 3

    mems = get_param(param_count, ip, param, mem)

    # target is always in position mode, so don't use the value retrieved and write directly to mem
    mem[mem[ip+3]] = mems[0] + mems[1]

    return ip + param_count + 1


### OP CODE = 2
# MULTIPLY
def multiply(ip, param, mem, *args):
    param_count = 3

    mems = get_param(param_count, ip, param, mem)

    # target is always in position mode, so don't use the value retrieved and write directly to mem
    mem[mem[ip+3]] = mems[0] * mems[1]

    return ip + param_count + 1


### OP CODE = 3
# INPUT
def input_f(ip, param, mem, *args):

    param_count = 1

    # get input - pop the first element from the phases input
    s = args[0].pop(0)
    #print('IP: {} -- INPUT: popped {}, remaining: {}'.format(ip, s, args[0]))

    mem[mem[ip+1]] = s

    return ip + param_count + 1


### OP CODE = 4
# OUTPUT
def output_f(ip, param, mem, *args):
    ## TO DO: modify to store output in global stack
    param_count = 1

    mems = get_param(param_count, ip, param, mem)
    out = mems[0]

    # store the output value in the 2nd place of the phases (1st place is next phase value)
    args[0].insert(1, out)

    #print('IP: {} -- OUTPUT: {}, phases: {}'.format(ip, out, args[0]))

    return ip + param_count + 1


### OP CODE = 5
# JUMP IF TRUE
def jump_if_true(ip, param, mem, *args):
    param_count = 2

    mems = get_param(param_count, ip, param, mem)

    #print('IP: {} __ jump-if-true: {}'.format(ip, mems[0]))

    if mems[0] != 0:
        ip = mems[1]
    else:
        ip += param_count + 1

    return ip


### OP CODE = 6
# JUMP IF FALSE
def jump_if_false(ip, param, mem, *args):
    param_count = 2

    mems = get_param(param_count, ip, param, mem)

    #print('IP: {} __ jump-if-false: {}'.format(ip, mems[0]))

    if mems[0] == 0:
        ip = mems[1]
    else:
        ip += param_count + 1

    return ip


### OP CODE = 7
# LESS THAN
def less_than(ip, param, mem, *args):
    param_count = 3

    mems = get_param(param_count, ip, param, mem)

    #print('IP: {} __ less-than: {} < {}'.format(ip, mems[0], mems[1]))

    mem[mem[ip+3]] = int(mems[0] < mems[1])

    return ip + param_count + 1


### OP CODE = 8
# EQUAL
def equals(ip, param, mem, *args):
    param_count = 3

    mems = get_param(param_count, ip, param, mem)

    #print('IP: {} __ equal: {} < {}'.format(ip, mems[0], mems[1]))

    mem[mem[ip+3]] = int(mems[0] == mems[1])

    return ip + param_count + 1


### OP CODE = 99
# HALT
def halt(ip, param, mem, *args):
    #print('IP: {} ### HALT ###'.format(ip))
    return -1



opcodes = {
    1: add, 
    2: multiply, 
    3: input_f, 
    4: output_f, 
    5: jump_if_true, 
    6: jump_if_false, 
    7: less_than,
    8: equals,
    99: halt}



def get_opcode(opcode):
    ops = str(opcode).zfill(6)
    # decode opcode - get last two digits
    op = int(ops[-2:])
    param = ops[:-2]
    
    return param, op

def run_intcode(mem, phases):
    ip = 0
    while (ip != -1):
        # get opcode and parameter mode instructions
        param, op = get_opcode(mem[ip])

        # execute the opcode
        params = [ip, param, mem]
        if op in [3, 4]:
            params.append(phases)
        ip = opcodes[op](*params)

# read input
f_name = 'input.txt'
inp = list(map(int, open(f_name).readline().split(',')))

print('PART 1: Starting!')

results = dict()
for p in permutations(range(5)):
    # take a copy of the phases to store
    temp_phase = p[:]

    # create a list (permutations gives you a tuple)
    phases = list(p)

    # add the initial input signal 0 for the first run
    phases.insert(1, 0)

    for _ in range(5):
        mem_copy = inp[:]
        run_intcode(mem_copy, phases)

    # retrieve result
    res = phases[0]

    print('Result for {}: {}'.format(temp_phase, res))
    results[temp_phase] = res

# get max from dictionary
max_key = max(results, key=results.get)
print('-- Max phase: {}, output: {}'.format(max_key, results[max_key]))

print('PART 1: End!')