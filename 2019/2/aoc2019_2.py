examples = ['1,9,10,3,2,3,11,0,99,30,40,50', '1,0,0,0,99', '2,4,4,5,99,0', '1,1,1,4,99,5,6,0,99']
num_examples = [list(map(int, ex.split(','))) for ex in examples]



input = list(map(int, open('input.txt').readline().split(',')))



def add(ip, mem):
    mem[mem[ip+3]] = mem[mem[ip+1]] + mem[mem[ip+2]]
    return ip + 4

def multiply(ip, mem):
    mem[mem[ip+3]] = mem[mem[ip+1]] * mem[mem[ip+2]]
    return ip + 4

def halt(ip, mem):
    return -1

opcodes = {1: add, 2: multiply, 99: halt}

def run_intcode(mem):
    ip = 0
    while (ip != -1):
        opcode = mem[ip]
        ip = opcodes[opcode](ip, mem)

    return mem[0]

def initialize_mem(init_mem, noun, verb):
    temp_mem = init_mem[:]
    temp_mem[1] = noun
    temp_mem[2] = verb
    return temp_mem

noun = 12
verb = 2
mem = initialize_mem(input, noun, verb)

print('Part 1: ', run_intcode(mem))

#### part 2
# Find noun / verb for output 19690720

target = 19690720

for noun in range(0, 100):
    for verb in range(0, 100):
        mem = initialize_mem(input, noun, verb)
        if run_intcode(mem) == target:
            print('Part 2. Noun: {}, verb {}, answer {}'.format(noun, verb, 100 * noun + verb))
            break

