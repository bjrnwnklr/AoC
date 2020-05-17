from collections import defaultdict
import logging
from string import ascii_lowercase






class InputInterrupt(Exception):
    pass

class OutputInterrupt(Exception):
    pass


class Duet():
    
    def __init__(self, prgrm, pg_id=0):
        
        # the program
        self.prgrm = prgrm
        
        # registers
        self.regs = defaultdict(int)

        # waiting flag
        self.wait = False

        # alive flag
        self.alive = True

        # how many times did we send a message?
        self.snd_count = 0

        # how many times was mul called?
        self.mul_count = 0

        # instruction pointer
        self.ip = 0
        # length of program
        self.pg_length = len(prgrm)
        # program id
        self.pg_id = pg_id
        self.regs['p'] = pg_id

        logging.info(f'[P{self.pg_id}] starting. Length: {self.pg_length}.')

    def get_val(self, y):
        # determine if y is a value or a register
        if y in ascii_lowercase:
            return self.regs[y]
        else:
            return int(y)

    def run_pg(self):
        # run program as long as IP is within program boundaries
        while 0 <= self.ip < self.pg_length:
            line = self.prgrm[self.ip].split(' ')
            instr = line[0]

            if instr == 'snd':
                # send signal to other program
                x = self.get_val(line[1])
                # determine program id to send to
                other_prgrm = (self.pg_id + 1) % 2
                msg_queues[other_prgrm].append(x)
                # increase send counter so we know how many times we sent something
                self.snd_count += 1
                logging.debug(f'[P{self.pg_id}][{self.ip}]: Sending to P{other_prgrm}: {x}.')

                self.ip += 1
            elif instr == 'set':
                # set register X to value of Y (Y can be value or register)
                x = line[1]
                y = self.get_val(line[2])
                self.regs[x] = y
                logging.debug(f'[P{self.pg_id}][{self.ip}]: Set: regs[{x}] = {y}.')

                self.ip += 1
            elif instr == 'add':
                x = line[1]
                y = self.get_val(line[2])
                self.regs[x] += y
                logging.debug(f'[P{self.pg_id}][{self.ip}]: Add: regs[{x}] += {y}. {self.regs[x]}')

                self.ip += 1
            elif instr == 'sub':
                x = line[1]
                y = self.get_val(line[2])
                self.regs[x] -= y
                logging.debug(f'[P{self.pg_id}][{self.ip}]: Sub: regs[{x}] -= {y}. {self.regs[x]}')

                self.ip += 1
            elif instr == 'mul':
                x = line[1]
                y = self.get_val(line[2])
                self.regs[x] *= y
                logging.debug(f'[P{self.pg_id}][{self.ip}]: Mul: regs[{x}] *= {y}. {self.regs[x]}')
                # for part 1, we count how many times mul is called.
                self.mul_count += 1

                self.ip += 1
            elif instr == 'mod':
                x = line[1]
                y = self.get_val(line[2])
                self.regs[x] %= y
                logging.debug(f'[P{self.pg_id}][{self.ip}]: Mod: regs[{x}] %= {y}. {self.regs[x]}')

                self.ip += 1
            elif instr == 'rcv':
                x = line[1]

                if msg_queues[self.pg_id]:
                    # if something in our queue, get the first msg
                    val = msg_queues[self.pg_id].pop(0)
                    logging.debug(f'[P{self.pg_id}][{self.ip}]: Received {val}')
                    self.regs[x] = val
                    self.ip += 1
                else:
                    self.wait = True
                    # call interrupt if we have to wait
                    raise InputInterrupt
                
            elif instr == 'jgz':
                x = self.get_val(line[1])
                y = self.get_val(line[2])
                logging.debug(f'[P{self.pg_id}][{self.ip}]: Jgz: {x} > 0')
                if x > 0:
                    self.ip += y
                    logging.debug(f'[P{self.pg_id}][{self.ip}]: jumping by {y} to {self.ip}.')
                else:
                    self.ip += 1
            elif instr == 'jnz':
                x = self.get_val(line[1])
                y = self.get_val(line[2])
                logging.debug(f'[P{self.pg_id}][{self.ip}]: Jnz: {x} != 0')
                if x != 0:
                    self.ip += y
                    logging.debug(f'[P{self.pg_id}][{self.ip}]: jumping by {y} to {self.ip}.')
                else:
                    self.ip += 1


        self.alive = False
        logging.info(f'[P{self.pg_id}][{self.ip}]: Terminated. Sent {self.snd_count} msgs.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        prgrm = [line.strip('\n') for line in f.readlines()]

    # two message queues, both empty
    msg_queues = [[], []]

    # create two programs
    duets = Duet(prgrm[:]) 

    if duets.alive:
        duets.run_pg()

    print(f'Finished. Mul was called {duets.mul_count} times.')

    # part 1: 9409