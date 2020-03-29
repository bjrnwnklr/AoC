# Synacor challenge

# first attempt at creating the virtual machine

from collections import defaultdict, deque
import logging
import numpy as np
# import pickle
from datetime import datetime
import json

def read_bin(f_name):
    logging.info(f'Reading file {f_name} as binary.')
    with open(f_name, 'rb') as f:
        data = f.read()
        int_data = list(np.frombuffer(data, dtype=np.uint16).astype(int))
        # convert to int
        int_data = [int(x) for x in int_data]

    if len(int_data) > 0:
        return int_data
    else:
        raise ValueError(f'While reading from {f_name}, no data was found.')


def load_json(vm_state):
    print('Loading VM state. Current state is:')
    # we now have a json dictionary and need to unpack it
    ip = vm_state['ip']
    print(f'ip: {ip}')

    done = vm_state['done']
    print(f'done: {done}')

    registers = vm_state['registers']
    print(f'registers: {registers}')

    stack = vm_state['stack']
    print(f'stack: {stack}')
    
    inp_buffer = vm_state['inp_buffer']
    print(f'inp_buffer: {inp_buffer}')

    mem_tmp = vm_state['mem']
    mem = {int(k): v for k, v in mem_tmp.items()}
    print(f'mem: length: {len(mem)}')

    mem_copy_tmp = vm_state['mem_copy']
    mem_copy = {int(k): v for k, v in mem_copy_tmp.items()}
    print(f'mem_copy: length: {len(mem_copy)}')

    return ip, done, mem, mem_copy, registers, stack, inp_buffer   

class Synacor():

    # global variables
    # modulo - 16 bit
    MOD = 32768

    def __init__(self, mem=dict(), mem_copy=dict(), ip=0, done=False, registers=[0, 0, 0, 0, 0, 0, 0, 0], stack=[], inp_buffer=[]):

        # instruction pointer
        self.ip = ip

        # halt parameter
        self.done = done

        # defaultdict of the program
        self.mem = defaultdict(int, mem)
        self.mem_copy = defaultdict(int, mem_copy)

        # registers (0 - 7)
        self.registers = registers

        # stack
        self.stack = deque(stack)

        # input buffer
        self.inp_buffer = deque(inp_buffer)

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

        self._op_names = {
            0: ('halt', 0),
            1: ('set', 3),
            2: ('push', 2),
            3: ('pop', 2),
            4: ('eq', 4),
            5: ('gt', 4),
            6: ('jmp', 2),
            7: ('jt', 3),
            8: ('jf', 3),
            9: ('add', 4),
            10: ('mult', 4),
            11: ('mod', 4),
            12: ('and', 4),
            13: ('or', 4),
            14: ('not', 3),
            15: ('rmem', 3),
            16: ('wmem', 3),
            17: ('call', 2),
            18: ('ret', 0),
            19: ('out', 2),
            20: ('in', 2),
            21: ('noop', 0)
        }

        # godmode commands
        self.godmode_commands = [
            'save',
            'exit',
            'debug',
            'info',
            'nolog',
            'mem',
            'peek',
            'poke',
            'code',
            'patch_teleport'
        ]

    

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


    # input processing, including godmode switch
    def _input_parser(self):

        # prompt function - show a (g) if we are in godmode
        def _prompt():    
            # get current location
            loc = self.mem[2732]  
            return f"{'(g) ' if godmode_flag else ''}[{loc}] Input > "

        godmode_flag = False

        # get input until we have a non-godmode input
        while True:

            inp = input(_prompt())
            
            # process godmode commands if we are in godmode, 
            # switch to godmode if keyword 'g' given as input,
            # otherwise return input
            if godmode_flag:
                if inp in self.godmode_commands:
                    if inp == 'exit':
                        godmode_flag = False
                    elif inp == 'info':
                        print('---INFO---')
                        print(f'IP:\t\t{self.ip}')
                        print(f'Registers:\t{self.registers}')
                    elif inp == 'debug':
                        print('Turning on DEBUG logging.')
                        logging.getLogger().setLevel(logging.DEBUG)
                    elif inp == 'nolog':
                        print('Turning off DEBUG logging.')
                        logging.getLogger().setLevel(logging.CRITICAL)
                    elif inp == 'save':
                        # save the class instance to a pickle file
                        self._save_json()
                    elif inp == 'mem':
                        print('Memory compare.')
                        # compare memory
                        self._mem_compare()
                    elif inp == 'code':
                        self._dump_code()
                    elif inp == 'patch_teleport':
                        self._patch_teleport()
                elif inp[:4] == 'peek':
                    # get numeric part of input command
                    _, address = inp.split(' ')
                    address = int(address)
                    # look at memory at address
                    self._peek(address)
                elif inp[:4] == 'poke':
                    _, address, value = inp.split(' ')
                    address = int(address)
                    value = int(value)
                    self._poke(address, value)
                elif inp[:4] == 'setr':
                    _, reg, value = inp.split(' ')
                    reg = int(reg)
                    value = int(value)
                    self.registers[reg] = value
                elif inp[:5] == 'print':
                    _, addr, print_func_code, key = inp.split(' ')
                    addr = int(addr)
                    print_func_code = int(print_func_code)
                    key = int(key)
                    self._decode_print(addr, print_func_code, key)
                else:
                    print(f'Unknown godmode command "{inp}". Try again or type "help" for a list of commands.')                
            elif inp == 'g':
                # activate godmode when the 'g' command is given at the standard prompt
                print('Activating godmode. Type "exit" to leave godmode.')
                godmode_flag = True
            else:
                # godmode not activated, so assume input was a standard input. 
                # Don't ask for additional input, just pass through what we got.
                break            
               
        # create a copy of the current memory
        self.mem_copy = self.mem.copy()

        return inp


    ###########
    #
    # GODMODE utility functions

    # dump memory into a new file and generate pseudocode from it
    def _dump_code(self):

        # some utility functions to extract Ascii values and registers
        def _decode_mem(val):
            # check if register
            if 32768 <= val <= 32775:
                decoded_val = f'r{val - 32768}'
            elif 32 <= val <= 126:
                decoded_val = f'{val:>3} ( {chr(val)} )'
            else:
                decoded_val = val
            return decoded_val

        curr_time = datetime.strftime(datetime.now(), '%Y%m%d_%H%M')
        f_name_code = f'{curr_time}_code.txt'
        f_name_text = f'{curr_time}_text.txt'
        print(f'Saving code to "{f_name_code}".')

        ip = 0
        code_end = 6067
        ip_max = max(self.mem.keys())
    
        with open(f_name_code, 'w') as f:
            # iterate through memory from 0 to highest memorey value
            while ip <= code_end:
                # retrieve the value at the mem position
                cmd = self.mem[ip]
                # if it is a known opcode, get the number of paramaters and write out the command with paramaters
                if cmd in self._op_names:
                    ip_name, param_count = self._op_names[cmd]
                    op_param_text = ' '.join(f'{_decode_mem(self.mem[ip + i])}' for i in range(1, param_count))
                    f.write(f'[{ip:>6}]\t{ip_name} {op_param_text}\n')
                    # take care of 'halt' (0), 'ret' (18) and 'noop' (21) opcodes, who have no parameters - move by 1 if encountered
                    if cmd in [0, 18, 21]:
                        param_count = 1
                else:
                    f.write(f'[{ip:>6}]\t{_decode_mem(self.mem[ip])}\n')
                    param_count = 1
                ip += param_count
        # we are now above the code end, only text follows from here. Print it to a different file.
        print(f'Saving text to "{f_name_text}".')
        with open(f_name_text, 'w') as f:
            while ip <= ip_max:
                c = self.mem[ip]
                if 0 <= c <= 126:
                    f.write(chr(self.mem[ip]))
                ip += 1


    
    # print decoder
    def _decode_print(self, length_addr, print_func_code, key):
        
        def _decode_1531(char, key):
            return (char | key) & (0x7fff ^ (char & key))
        
        p_funcs = {
            1531: _decode_1531
        }
        
        # get number of characters to print
        num_chars = self.mem[length_addr]
        # get all characters
        chars = [self.mem[length_addr + i] for i in range(1, num_chars + 1)]

        if print_func_code in p_funcs:
            # get print function
            p_func = p_funcs[print_func_code]
            # print text
            print(''.join(chr(p_func(char, key)) for char in chars))

    # patch memory for teleporting
    def _patch_teleport(self):
        # set r7 to teleport energy level (still need to find right level)
        self.registers[7] = 25734
        # write instructions into memory at 5478-5482 to jump over the confirmation code
        # 'set' register 0 to 6
        self.mem[5478] = 1
        self.mem[5479] = 32768
        self.mem[5480] = 6
        # 'jmp' to 5491 (the address after the calculation. r0 has to be 6 for this)
        self.mem[5481] = 6
        self.mem[5482] = 5491

    # save state of VM into a JSON file
    def _save_json(self):
        # create new object: dict of all the various state objects we want to save
        state = {
            'ip': int(self.ip),
            'done': self.done,
            'mem': self.mem,
            'mem_copy': self.mem_copy,
            'registers': self.registers,
            'stack': list(self.stack),
            'inp_buffer': list(self.inp_buffer)
        }

        # get current time
        curr_time = datetime.strftime(datetime.now(), '%Y%m%d_%H%M')
        f_name = f'{curr_time}_synacor.json'
        print(f'Saving current state to "{f_name}".')
        with open(f_name, 'w') as f:
            json.dump(state, f)

    # compare current memory with memory dump and show differences
    def _mem_compare(self):
        # convert current memory and memory copy into numpy arrays for quick comparison
        mem_array = np.array(list(self.mem.values()))
        mem_c_array = np.array(list(self.mem_copy.values()))

        # create an indexing array with differences
        diffs = mem_array != mem_c_array
        diff_index = np.flatnonzero(diffs)

        print(f'Found {len(diff_index)} differences.')

        # get list of indices with differences
        diff_list = list(diff_index)

        # print out differences
        print('Index\tPrevMem\tCurrMem')
        for n in diff_list:
            print(f'[{n}]\t{self.mem_copy[n]}\t{self.mem[n]}')

    # peek at a memory address
    def _peek(self, address):
        peek_window = 10
        if 0 <= address <= self.MOD:
            print('Addr\tValue')
            for i in range(max(0, address - peek_window), address):
                print(f'[{i}]\t{self.mem[i]}')
            print(f'[{address}]\t{self.mem[address]}\t<---')
            for i in range(address + 1, min(self.MOD, address + peek_window + 1)):
                print(f'[{i}]\t{self.mem[i]}')
        else:
            print(f'Incorrect address: {address}')
            
    # write value to a memory address
    def _poke(self, address, value):
        if 0 <= address <= self.MOD:
            print(f'[{address}]\t{self.mem[address]}\t{value}')
            self.mem[address] = value
        else:
            print(f'Incorrect address: {address}')

    ################
    #
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
            b = self._input_parser()
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




