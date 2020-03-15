# Synacor challenge

# first attempt at creating the virtual machine

from collections import defaultdict
import logging
import numpy as np

# utility functions

def is_valid(i):
    return 0 <= i <= 32775

def is_literal(i):
    return 0 <= i <= 32767

def is_register(i):
    return 32768 <= i <= 32775

def reg_num(i):
    if is_register(i):
        return i - 32768
    else:
        return -1



def read_bin(f_name):
    logging.info(f'Reading file {f_name} as binary.')
    with open(f_name, 'rb') as f:
        data = f.read()
        int_data = list(np.frombuffer(data, dtype=np.uint16))

    if len(int_data) > 0:
        return int_data
    else:
        raise ValueError(f'While reading from {f_name}, no data was found.')

class Synacor():

    # global variables
    # modulo - 16 bit
    MOD = 32768

    def __init__(self, mem=[], ip=0):

        # instruction pointer
        self.ip = 0

        # halt parameter
        self.done = False

        # defaultdict of the program
        self.mem = defaultdict(int, enumerate(mem))

        # set up registers, value = 0
        self.registers = [0 for _ in range(8)]

        # list of opcodes
        # format: 
        # - function to execute
        # - number of arguments (including the instruction itself)
        self.opcodes = {
            0: (self._halt, 0),
            19: (self._out, 2),
            21: (self._noop, 0)
        }


    # evaluate parameter - if valid, literal or register
    def _run(self):
        while (not self.done):
            # retrieve the executable method, read / write addresses, number of params
            # from the current memory address
            op_command, params, param_count = self._get_opcode(self.mem[self.ip])

            # execute the opcode command
            op_command(params, param_count)

    def _get_opcode(self, opcode):

        def _mem_mode(self, m):
            if is_valid(m):
                return 0 if 0 <= m <= 32767 else 1

        # get the opcode from the list of opcodes
        if opcode in self.opcodes:
            op_command, param_count = self.opcodes[opcode]

            # get the parameters / addresses
            params = [
                self.mem[self.ip + i] for i in range(1, param_count)
            ]

            return op_command, params, param_count

        else:
            raise ValueError(f'Wrong opcode, or not yet implemented: {opcode}')


    # opcode functions

    # 0: halt
    def _halt(self, params, param_count):
        logging.debug(f'IP: {self.ip}: ### HALT ###')
        self.done = True

    # 19: out
    def _out(self, params, param_count):
        logging.debug(f'IP: {self.ip}: out')
        print(chr(params[0]), end='')
        
        self.ip += param_count

    # 21: noop
    def _noop(self, params, param_count):
        logging.debug(f'IP: {self.ip}: noop')
        self.ip += 1




