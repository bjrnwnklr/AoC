from collections import deque
import logging

class Assembunny:
    def __init__(self, program, reg_a):
        self.program = program
        self.regs = {
            'a': reg_a,
            'b': 0,
            'c': 0,
            'd': 0
        }
        self.ip = 0
        self.end = len(self.program)
        self.outq = deque([])

    def get_reg(self, a):
        if a in 'abcd':
            return self.regs[a]
        else:
            return int(a)

    def _repr_regs(self):
        return f'[{", ".join(map(str, self.regs.values()))}]'

    def run(self):
        while self.ip < self.end:
            line = program[self.ip]
            cmd = line[0]
            logging.debug(f'[{self.ip:03}]{self._repr_regs()}: {line}')
            if cmd == 'cpy':
                val = self.get_reg(line[1])
                self.regs[line[2]] = val
                self.ip += 1
            elif cmd == 'inc':
                self.regs[line[1]] += 1
                self.ip += 1
            elif cmd == 'dec':
                self.regs[line[1]] -= 1
                self.ip += 1
            elif cmd == 'jnz':
                val = self.get_reg(line[1])
                if val != 0:
                    self.ip += self.get_reg(line[2])
                else:
                    self.ip += 1
            elif cmd == 'tgl':
                a = self.get_reg(line[1])
                # get the instruction at program[a] - we need to change this
                target_ip = self.ip + a
                if target_ip < self.end:
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
                self.ip += 1
            elif cmd == 'out':
                val = self.get_reg(line[1])
                self.outq.append(val)
                self.ip += 1
                break


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='asm.log', filemode='w')

    f_name = 'input.txt'
    # f_name = 'ex1.txt'

    with open(f_name, 'r') as f:
        program = [line.strip('\n').split(' ') for line in f.readlines()]

    # find the lowest value for reg a to produce a repeating 0, 1, 0, 1, ... output stream
    # This aborts as soon as the output pattern diverts from 0, 1, 0, 1 and prints out
    # WRONG
    # Program will run infinitely as soon as the right number has been found.
    for n in range(200):
        asm = Assembunny(program[:], n)
        print(f'{n:03}')
        wrong = False
        out_count = 0
        while not wrong:
            asm.run()
            out_val = asm.outq.popleft()
            if out_count % 2 != out_val:
                wrong = True
            out_count += 1
        print('WRONG!')

# Part 1: 158 produces a signal of 0, 1, 0, 1, 0, 1 etc
