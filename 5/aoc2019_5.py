#examples = ['1,9,10,3,2,3,11,0,99,30,40,50', '1,0,0,0,99', '2,4,4,5,99,0', '1,1,1,4,99,5,6,0,99']
#num_examples = [list(map(int, ex.split(','))) for ex in examples]




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
def add(ip, param, mem):
    param_count = 3

    mems = get_param(param_count, ip, param, mem)

    # target is always in position mode, so don't use the value retrieved and write directly to mem
    mem[mem[ip+3]] = mems[0] + mems[1]

    return ip + param_count + 1


### OP CODE = 2
# MULTIPLY
def multiply(ip, param, mem):
    param_count = 3

    mems = get_param(param_count, ip, param, mem)

    # target is always in position mode, so don't use the value retrieved and write directly to mem
    mem[mem[ip+3]] = mems[0] * mems[1]

    return ip + param_count + 1


### OP CODE = 3
# INPUT
def input_f(ip, param, mem):
    param_count = 1
    # request input
    s = int(input('IP: {} -- Input: '.format(ip)))

    mem[mem[ip+1]] = s

    return ip + param_count + 1


### OP CODE = 4
# OUTPUT
def output_f(ip, param, mem):
    param_count = 1

    mems = get_param(param_count, ip, param, mem)

    print('IP: {} -- OUTPUT: {}'.format(ip, mems[0]))

    return ip + param_count + 1


### OP CODE = 5
# JUMP IF TRUE
def jump_if_true(ip, param, mem):
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
def jump_if_false(ip, param, mem):
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
def less_than(ip, param, mem):
    param_count = 3

    mems = get_param(param_count, ip, param, mem)

    #print('IP: {} __ less-than: {} < {}'.format(ip, mems[0], mems[1]))

    mem[mem[ip+3]] = int(mems[0] < mems[1])

    return ip + param_count + 1


### OP CODE = 8
# EQUAL
def equals(ip, param, mem):
    param_count = 3

    mems = get_param(param_count, ip, param, mem)

    #print('IP: {} __ equal: {} < {}'.format(ip, mems[0], mems[1]))

    mem[mem[ip+3]] = int(mems[0] == mems[1])

    return ip + param_count + 1


### OP CODE = 99
# HALT
def halt(ip, param, mem):
    print('IP: {} ### HALT ###'.format(ip))
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

def run_intcode(mem):
    ip = 0
    while (ip != -1):
        # get opcode and parameter mode instructions
        param, op = get_opcode(mem[ip])

        # execute the opcode
        ip = opcodes[op](ip, param, mem)

# read input
inp = list(map(int, open('input.txt').readline().split(',')))

# take a copy of the input
mem_copy = inp[:]

print('PART 1: Starting! (Input: 1)')

run_intcode(mem_copy)

print('PART 1: Program ended!')

# part 1: 5346030


# take a copy of the input
mem_copy = inp[:]

print('PART 2: Starting! (Input: 5)')

run_intcode(mem_copy)

print('PART 2: Program ended!')

