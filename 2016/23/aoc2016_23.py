def get_reg(a):
    if a in 'abcd':
        return regs[a]
    else:
        return int(a)


if __name__ == '__main__':

    f_name = 'input.txt'
    # f_name = 'ex1.txt'

    with open(f_name, 'r') as f:
        program = [line.strip('\n').split(' ') for line in f.readlines()]

    # change c to 0 for part 1 and to 1 for part 2
    regs = {
        'a': 7,
        'b': 0,
        'c': 0,
        'd': 0
    }

    ip = 0
    end = len(program)

    while ip < end:
        line = program[ip]
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
                ip += get_reg(line[2])
            else:
                ip += 1
        elif cmd == 'tgl':
            a = get_reg(line[1])
            # get the instruction at program[a] - we need to change this
            target_ip = ip + a
            if target_ip < end:
                target_ins = program[target_ip]
                if len(target_ins) == 2:
                    # one argument instruction
                    if target_ins[0] == 'inc':
                        target_ins[0] = 'dec'
                    else:
                        target_ins[0] = 'inc'
                elif len(target_ins) == 3:
                    # two argument instruction
                    if target_ins[0] == 'jnz':
                        target_ins[0] = 'cpy'
                    else:
                        target_ins[0] = 'jnz'
            ip += 1

    print(f'Done, reg a value = {regs["a"]}')

    # Part 1: 10365
    
