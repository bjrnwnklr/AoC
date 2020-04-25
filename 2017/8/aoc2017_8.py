from collections import defaultdict
import operator


f_name = 'input.txt'

conditions = {
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne
}

inc_dec = {
    'inc': operator.add,
    'dec': operator.sub
}

registers = defaultdict(int)
max_val = 0

with open(f_name, 'r') as f:
    instructions = [l.strip('\n') for l in f.readlines()]

for instruction in instructions:
    register, instr, amount, _, cond_reg, cond, cond_val = instruction.split(' ')
    amount = int(amount)
    cond_val = int(cond_val)
    if conditions[cond](registers[cond_reg], cond_val):
        registers[register] = inc_dec[instr](registers[register], amount)

    # part 2, get the highest value held in registers
    curr_max = max(registers.values())
    if curr_max > max_val:
        max_val = curr_max


sorted_registers = sorted(registers.keys(), key=registers.get, reverse=True)

print(sorted_registers)
print(registers)
print(sorted_registers[0], registers[sorted_registers[0]])

print(f'Highest value held in registers: {max_val}.')

# Part 1: a: 3089
# Part 2: 5391
