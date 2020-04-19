
f_name = 'input.txt'

with open(f_name, 'r') as f:
    instructions = [int(x) for x in f.readlines()]

instr_p2 = instructions[:]

ip = 0
high_mem = len(instructions)
steps = 0

while -1 < ip < high_mem:
    # print(f'IP: {ip}. Instruction: {instructions[ip]}.')
    # get jump instruction
    jmp = instructions[ip]
    # increase current instruction by 1
    instructions[ip] += 1
    # jump to instruction
    ip += jmp
    # increment step counter
    steps += 1

print(f'Jumped to {ip} after {steps} steps.')


# Part 1: Jumped to 1056 after 358131 steps.

ip = 0
high_mem = len(instr_p2)
steps = 0

while -1 < ip < high_mem:
    # print(f'IP: {ip}. Instruction: {instructions[ip]}.')
    # get jump instruction
    jmp = instr_p2[ip]
    # increase current instruction by 1
    if jmp >= 3:
        instr_p2[ip] -= 1
    else:
        instr_p2[ip] += 1
    # jump to instruction
    ip += jmp
    # increment step counter
    steps += 1

print(f'Jumped to {ip} after {steps} steps.')

# Part 2: Jumped to 1056 after 25558839 steps.