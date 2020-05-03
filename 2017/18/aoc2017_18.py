from collections import defaultdict
import logging
from string import ascii_lowercase

def get_val(y):
    # determine if y is a value or a register
    if y in ascii_lowercase:
        return regs[y]
    else:
        return int(y)


logging.basicConfig(level=logging.DEBUG)

f_name = 'input.txt'

with open(f_name, 'r') as f:
    prgrm = [line.strip('\n') for line in f.readlines()]

# registers
regs = defaultdict(int)
# sounds played
sounds = []
# instruction pointer
ip = 0
# length of program
pg_length = len(prgrm)
logging.debug(f'Starting. Program length: {pg_length}')

# run program as long as IP is within program boundaries
while 0 <= ip <= pg_length:
    line = prgrm[ip].split(' ')
    instr = line[0]

    if instr == 'snd':
        # play a sound - add to sounds
        x = get_val(line[1])
        sounds.append(x)
        logging.debug(f'[{ip}]: Sound played: {x}.')

        ip += 1
    elif instr == 'set':
        # set register X to value of Y (Y can be value or register)
        x = line[1]
        y = get_val(line[2])
        regs[x] = y
        logging.debug(f'[{ip}]: Set: regs[{x}] = {y}.')

        ip += 1
    elif instr == 'add':
        x = line[1]
        y = get_val(line[2])
        regs[x] += y
        logging.debug(f'[{ip}]: Add: regs[{x}] += {y}. {regs[x]}')

        ip += 1
    elif instr == 'mul':
        x = line[1]
        y = get_val(line[2])
        regs[x] *= y
        logging.debug(f'[{ip}]: Mul: regs[{x}] *= {y}. {regs[x]}')

        ip += 1
    elif instr == 'mod':
        x = line[1]
        y = get_val(line[2])
        regs[x] %= y
        logging.debug(f'[{ip}]: Mod: regs[{x}] %= {y}. {regs[x]}')

        ip += 1
    elif instr == 'rcv':
        if regs[line[1]]:
            print(f'[{ip}]: Recovered sound: {sounds[-1]}')

            # stop program once the first sound is recovered
            break
        ip += 1
    elif instr == 'jgz':
        x = line[1]
        y = get_val(line[2])
        logging.debug(f'[{ip}]: Jgz: regs[{x}] = {regs[x]}')
        if regs[line[1]] > 0:
            ip += get_val(line[2])
            logging.debug(f'[{ip}]: jumping by {y} to {ip}.')
        else:
            ip += 1


# Part 1: 3188

