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
        int_data = list(np.frombuffer(data, dtype=np.uint16).astype(int))

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

        self.registers = [0 for i in range(8)]

        # stack
        self.stack = deque([])

        # input buffer
        self.inp_buffer = deque([])

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
            10: (self._mult, 4),
            11: (self._mod, 4),
            12: (self._and, 4),
            13: (self._or, 4),
            14: (self._not, 3),
            15: (self._rmem, 3),
            16: (self._wmem, 3),
            17: (self._call, 2),
            18: (self._ret, 0),
            19: (self._out, 2),
            20: (self._in, 2),
            21: (self._noop, 0)
        }

    def _get_reg(self, i):
        return i - self.MOD

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
            r = i if 0 <= i <= 32767 else self.registers[self._get_reg(i)]
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
        a = self._get_reg(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])
        logging.debug(f'IP: {self.ip}: set reg {a} to {b}')
        logging.debug(f'Registers: {self.registers}')

        self.registers[a] = b
        logging.debug(f'Registers: {self.registers}')

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
        if self.stack:
            a = self._get_reg(self.mem[params[0]])
            b = self.stack.pop()

            logging.debug(f'IP: {self.ip}: pop. {b} into {a}')
            logging.debug(f'Stack: {self.stack}')
            self.registers[a] = b

            self.ip += param_count
        else:
            raise ValueError(f'Stack is empty: IP {self.ip}')

    # 4: eq
    def _eq(self, params, param_count):
        a = self._get_reg(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: eq. {a}; {b} == {c}')
        self.registers[a] = 1 if b == c else 0

        self.ip += param_count

    # 5: gt
    def _gt(self, params, param_count):
        a = self._get_reg(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: gt. {a}; {b} > {c}')
        self.registers[a] = 1 if b > c else 0

        self.ip += param_count

    # 6: jmp
    def _jmp(self, params, param_count):
        a = self._get_val(self.mem[params[0]])
        logging.debug(f'IP: {self.ip}: jmp to {a}')

        self.ip = a

    # 7: jt
    def _jt(self, params, param_count):
        a = self._get_val(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])
        logging.debug(f'IP: {self.ip}: jt {a} to {b}')

        if a != 0:
            self.ip = b
        else:
            self.ip += param_count

    # 8: jf
    def _jf(self, params, param_count):
        a = self._get_val(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])
        logging.debug(f'IP: {self.ip}: jf {a} to {b}')

        if a == 0:
            self.ip = b
        else:
            self.ip += param_count

    # 9: add
    def _add(self, params, param_count):
        a = self._get_reg(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: add. {a} = {b} + {c}')
        self.registers[a] = (b + c) % self.MOD

        self.ip += param_count

    # 10: mult
    def _mult(self, params, param_count):
        a = self._get_reg(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: mult. {a} = {b} * {c}')
        self.registers[a] = (b * c) % self.MOD

        self.ip += param_count

    # 11: mod
    def _mod(self, params, param_count):
        a = self._get_reg(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: mod. {a} = {b} % {c}')
        self.registers[a] = b % c

        self.ip += param_count

    # 12: and
    def _and(self, params, param_count):
        a = self._get_reg(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: and. {a} = {b} & {c}')
        self.registers[a] = b & c

        self.ip += param_count

    # 13: or
    def _or(self, params, param_count):
        a = self._get_reg(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])
        c = self._get_val(self.mem[params[2]])

        logging.debug(f'IP: {self.ip}: or. {a} = {b} | {c}')
        self.registers[a] = b | c

        self.ip += param_count

    # 14: not
    def _not(self, params, param_count):
        a = self._get_reg(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])

        logging.debug(f'IP: {self.ip}: not. {a} = ~{b} ({0x7fff ^ b})')
        self.registers[a] = 0x7fff ^ b

        self.ip += param_count

    # 15: rmem
    def _rmem(self, params, param_count):
        a = self._get_reg(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])

        logging.debug(f'IP: {self.ip}: rmem. {a} = {self.mem[b]} (b = {b})')
        self.registers[a] = self.mem[b]

        self.ip += param_count

    # 16: wmem
    def _wmem(self, params, param_count):
        a = self._get_val(self.mem[params[0]])
        b = self._get_val(self.mem[params[1]])

        logging.debug(f'IP: {self.ip}: wmem. {self.mem[a]} = {b} (a = {a})')
        self.mem[a] = b

        self.ip += param_count

    # 17: call
    def _call(self, params, param_count):
        a = self._get_val(self.mem[params[0]])
        
        # push next instruction onto stack
        self.stack.append(self.ip + param_count)
        logging.debug(f'IP: {self.ip}: call to {a}')
        logging.debug(f'Stack: {self.stack}')

        # jump to a
        self.ip = a

    # 18: ret
    def _ret(self, params, param_count):
        if self.stack:
            a = self.stack.pop()
            logging.debug(f'IP: {self.ip}: ret. jump to {a}')
            logging.debug(f'Stack: {self.stack}')

            self.ip = a
        else:
            self.done = True
        

    # 19: out
    def _out(self, params, param_count):
        a = self._get_val(self.mem[params[0]])
        # logging.debug(f'IP: {self.ip}: out {chr(a)}')
        print(chr(a), end='')
        
        self.ip += param_count

    # 20: in
    def _in(self, params, param_count):
        a = self._get_reg(self.mem[params[0]])
        logging.info(f'IP: {self.ip}: in. Looking for input to {a}')
        
        # convert to ascii stream and save to a
        # put read input into a queue. If queue is not empty, add next character to a
        # if queue is empty, ask for input

        # check if input buffer is empty, request input then
        if not self.inp_buffer:
            b = input('Input > ')
            logging.info(f'IP: {self.ip}: in. inp_buffer empty, read {b}')

            self.inp_buffer.extend(b + '\n')

        # if there is something in the input buffer, pop the first element and write it to <a>
        if self.inp_buffer:
            c = self.inp_buffer.popleft()
            logging.info(f'IP: {self.ip}: in. Taking {c} from inp_buffer and writing to {a}.')
            self.registers[a] = ord(c)

        self.ip += param_count

    # 21: noop
    def _noop(self, params, param_count):
        logging.debug(f'IP: {self.ip}: noop')
        self.ip += 1




