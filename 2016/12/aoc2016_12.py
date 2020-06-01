

f_name = 'input.txt'
# f_name = 'ex1.txt'

with open(f_name, 'r') as f:
    program = [line.strip('\n') for line in f.readlines()]

# change c to 0 for part 1 and to 1 for part 2
regs = {
    'a': 0,
    'b': 0,
    'c': 1,
    'd': 0
}

ip = 0
end = len(program)


def get_reg(a):
    if a in 'abcd':
        return regs[a]
    else:
        return int(a)

while ip < end:
    line = program[ip].split(' ')
    cmd = line[0]
    if cmd == 'cpy':
        val = get_reg(line[1])
        regs[line[2]] = val
        ip += 1
    elif cmd == 'inc':
        regs[line[1]] += 1
        ip += 1
    elif cmd == 'dec':
        regs[line[1]] -= 1
        ip += 1
    elif cmd == 'jnz':
        val = get_reg(line[1])
        if val != 0:
            ip += int(line[2])
        else:
            ip += 1


print(f'Done, reg a value = {regs["a"]}')
        
# part 1: 317993
# part 2: 9227647