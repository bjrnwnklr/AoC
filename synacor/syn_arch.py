# Synacor challenge

# first attempt at creating the virtual machine

from collections import defaultdict, deque
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


        # stack
        self.stack = deque([])

        # list of opcodes
        # format: 
        # - function to execute
        # - number of arguments (including the instruction itself)
        self.opcodes = {
            0: (self._halt, 0),
            1: (self._set, 3),
            2: (self._push, 2),
            3: (self._pop, 2),
            4: (self._eq, 4),
            5: (self._gt, 4),
            6: (self._jmp, 2),
            7: (self._jt, 3),
            8: (self._jf, 3),
            9: (self._add, 4),
            12: (self._and, 4),
            13: (self._or, 4),
            14: (self._not, 3),
            19: (self._out, 2),
            21: (self._noop, 0)
        }

    def _get_val(self, i):
        """
        Get a value from memory. If value provided is < 32768, return literal value,
        otherwise return memory value (i.e. from register).

        Parameters:
        - i: value to check. If value < 32768, same value is returned, otherwise value 
            of respective register is returned.

        Returns:
        - value that is either a literal (same that was passed in),
            or the value that is stored in the respective register.
        """
        if 0 <= i <= 32775:
            r = i if 0 <= i <= 32767 else self.mem[i]
            logging.debug(f'Checking val {i}, returning {r}.')
            return r
        else:
            raise ValueError(f'Wrong number: {i}.')

    # evaluate parameter - if valid, literal or register
    def _run(self):
        while (not self.done):
            # retrieve the executable method, read / write addresses, number of params
            # from the current memory address
            op_command, params, param_count = self._get_opcode(self.mem[self.ip])

            # execute the opcode command
            op_command(params, param_count)

    def _get_opcode(self, opcode):

        # get the opcode from the list of opcodes
        if opcode in self.opcodes:
            op_command, param_count = self.opcodes[opcode]

            # get the parameters / addresses
            params = [
                self.ip + i for i in range(1, param_count)
            ]

            return op_command, params, param_count

        else:
            raise ValueError(f'Wrong opcode, or not yet implemented: {opcode}')


    # opcode functions

    # 0: halt
    def _halt(self, params, param_count):
        logging.debug(f'IP: {self.ip}: ### HALT ###')
        self.done = True

    # 1: set
    def _set(self, params, param_count):
        """Sets register <a> to value of <b>.
        Register <a> is calculated by taking the memory value of the ip counter,
        which should result in a number in [32768..32775]. Then subtract 32768
        to get the number of the register.
        
        Arguments:
            params {list} -- list of parameter references (i.e. an instruction pointer)
            param_count {int} -- number of parameters
        """
        a, b = self.mem[params[0]] - self.MOD, self._get_val(self.mem[params[1]])
        logging.debug(f'IP: {self.ip}: set reg {a} to {b}')
        logging.debug(f'Registers: {list(self.mem[x] for x in range(self.MOD, self.MOD + 8))}')

        self.mem[a + self.MOD] = b
        logging.debug(f'Registers: {list(self.mem[x] for x in range(self.MOD, self.MOD + 8))}')

        self.ip += param_count

    # 2: push
    def _push(self, params, param_count):
        a = self._get_val(self.mem[params[0]])
        self.stack.append(a)

        logging.debug(f'IP: {self.ip}: push {a}')
        logging.debug(f'Stack: {self.stack}')

        self.ip += param_count

    # 3: pop
    def _pop(self, params, param_count):
        b = self.stack.pop()
        a = self.mem[params[0]]

        logging.debug(f'IP: {self.ip}: pop. {b} into {a}')
        logging.debug(f'Stack: {self.stack}')
        self.mem[a] = b

        self.ip += param_count

    # 4: eq
    def _eq(self, params, param_count):
        a = self.mem[params[0]]
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: eq. {a}; {b} == {c}')
        self.mem[a] = 1 if b == c else 0

        self.ip += param_count

    # 5: gt
    def _gt(self, params, param_count):
        a = self.mem[params[0]]
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: gt. {a}; {b} > {c}')
        self.mem[a] = 1 if b > c else 0

        self.ip += param_count

    # 6: jmp
    def _jmp(self, params, param_count):
        a = self._get_val(self.mem[params[0]])
        logging.debug(f'IP: {self.ip}: jmp to {a}')

        self.ip = a

    # 7: jt
    def _jt(self, params, param_count):
        a, b = self._get_val(self.mem[params[0]]), self._get_val(self.mem[params[1]])
        logging.debug(f'IP: {self.ip}: jt {a} to {b}')

        if a != 0:
            self.ip = b
        else:
            self.ip += param_count

    # 8: jf
    def _jf(self, params, param_count):
        a, b = self._get_val(self.mem[params[0]]), self._get_val(self.mem[params[1]])
        logging.debug(f'IP: {self.ip}: jf {a} to {b}')

        if a == 0:
            self.ip = b
        else:
            self.ip += param_count

    # 9: add
    def _add(self, params, param_count):
        a = self.mem[params[0]]
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: add. {a} = {b} + {c}')
        self.mem[a] = (b + c) % self.MOD

        self.ip += param_count

    # 12: and
    def _and(self, params, param_count):
        a = self.mem[params[0]]
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: and. {a} = {b} & {c}')
        self.mem[a] = b & c

        self.ip += param_count

    # 13: or
    def _or(self, params, param_count):
        a = self.mem[params[0]]
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: or. {a} = {b} | {c}')
        self.mem[a] = b | c

        self.ip += param_count

    # 14: not
    def _not(self, params, param_count):
        a = self.mem[params[0]]
        b = self._get_val(self.mem[params[1]])

        logging.debug(f'IP: {self.ip}: not. {a} = ~{b}')
        self.mem[a] = ~b

        self.ip += param_count

    # 19: out
    def _out(self, params, param_count):
        a = self._get_val(self.mem[params[0]])
        # logging.debug(f'IP: {self.ip}: out {chr(a)}')
        print(chr(a), end='')
        
        self.ip += param_count

    # 21: noop
    def _noop(self, params, param_count):
        logging.debug(f'IP: {self.ip}: noop')
        self.ip += 1




