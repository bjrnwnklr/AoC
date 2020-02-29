# Intcode virtual machine (as of AoC2019, day 15)

from collections import deque, defaultdict
import logging
import math
from copy import deepcopy


class InputInterrupt(Exception):
    pass

class OutputInterrupt(Exception):
    pass


class Intcode():

    def __init__(self, mem=[], ip=0, rel_base=0, amp_id=1):
        # set ip to 0
        self.ip = ip

        # set relative base to 0
        self.rel_base = rel_base
        
        # set halt parameter
        self.done = False
        self.amp_id = amp_id
                  
        # create a defaultdict of the memory values to allow for positive addresses with 0 value
        self.mem = defaultdict(int, enumerate(mem))
        
        # input and output queues
        self.in_queue = deque()
        self.out_queue = deque()

        self.opcodes = {
            1: (self._add, 4),
            2: (self._multiply, 4), 
            3: (self._input_f, 2),
            4: (self._output_f, 2),
            5: (self._jump_if_true, 3),
            6: (self._jump_if_false, 3),
            7: (self._less_than, 4),
            8: (self._equals, 4),
            9: (self._adj_rel_base, 2),
            99: (self._halt, 0)}
  

    #### Main run function ####
    def _run_intcode(self):
        """
        Processes intcode commands until halt signal is received.
        """
        while (not self.done):
            # get executable intcode method, the number of parameters and the read/write addresses
            int_command, addresses, param_count = self._get_opcode(self.mem[self.ip])

            # execute the opcode
            int_command(addresses, param_count)


    #### Support functions ####
    def _get_opcode(self, opcode):
        """
        Retrieve opcode and parameter modes from memory, then evaluate parameter modes and return read/write 
        memory positions.

        Returns:
        - int_command: executable intcode methode, e.g. add
        - addresses: list of memory pointers for the read/write parameters
        - param_count: number of parameters used by the int_command
        """
        # pad opcode to 6 digits with zeroes
        ops = str(opcode).zfill(6)
        # decode opcode - opcode is last two digits, the rest are parameter modes
        op = int(ops[-2:])
        param_modes = ops[:-2]

        # get the executable function for the opcode and number of params
        int_command, param_count = self.opcodes[op]

        # get the read / write addresses based on parameter mode
        # 0 = position mode
        # 1 = immediate mode
        # 2 = relative mode
        addresses = [
            [self.mem[self.ip + i], self.ip + i, self.mem[self.ip + i] + self.rel_base][int(param_modes[-i])]
            for i in range(1, param_count)
        ]

        return int_command, addresses, param_count


    def run_input_output(self, input_signal):
        """
        Runs an input-output cycle on the intcode machine: 
        - Adds 1 input signal to the input queue
        - Runs intcode until an output is given
        - Returns the output.

        Returns:
        - Exactly 1 output from the intcode process.
        """
        self.in_queue.append(input_signal) 
        while(not self.done):   
            try:
                self._run_intcode()
            except(InputInterrupt):
                # do nothing
                pass
            except(OutputInterrupt):
                # read output and return output
                output = self.out_queue.popleft()
                break

        return output

    def clone(self):
        """
        Returns a deepcopy of the intcode VM with its current state - can be used to store the current state and use it later.

        Returns:
        - Deepcopy of the current intcode VM.
        """
        return deepcopy(self)

    #### OP CODE EXECUTION FUNCTIONS ####

    ### OP CODE = 1
    # ADD
    def _add(self, current_path, param_count):
        # Allow writing in both position and relative mode -- use 3rd parameter
        self.mem[current_path[2]] = self.mem[current_path[0]] + self.mem[current_path[1]]

        self.ip += param_count

    ### OP CODE = 2
    # MULTIPLY
    def _multiply(self, current_path, param_count):
        # Allow writing in both position and relative mode -- use 3rd parameter
        self.mem[current_path[2]] = self.mem[current_path[0]] * self.mem[current_path[1]]

        self.ip += param_count

    ### OP CODE = 3
    # INPUT
    def _input_f(self, current_path, param_count):
        # get input - 
        if self.in_queue:
            s = self.in_queue.popleft()

            self.mem[current_path[0]] = s
            
            self.ip += param_count

        else:
            raise InputInterrupt

    ### OP CODE = 4
    # OUTPUT
    def _output_f(self, current_path, param_count):
        # store message in message stack
        self.out_queue.append(self.mem[current_path[0]])

        self.ip += param_count

        # pause execution since we passed an output
        raise OutputInterrupt

    ### OP CODE = 5
    # JUMP IF TRUE
    def _jump_if_true(self, current_path, param_count):
        if self.mem[current_path[0]] != 0:
            self.ip = self.mem[current_path[1]]
        else:
            self.ip += param_count

    ### OP CODE = 6
    # JUMP IF FALSE
    def _jump_if_false(self, current_path, param_count):
        if self.mem[current_path[0]] == 0:
            self.ip = self.mem[current_path[1]]
        else:
            self.ip += param_count

    ### OP CODE = 7
    # LESS THAN
    def _less_than(self, current_path, param_count):
        self.mem[current_path[2]] = int(self.mem[current_path[0]] < self.mem[current_path[1]])

        self.ip += param_count

    ### OP CODE = 8
    # EQUAL
    def _equals(self, current_path, param_count):
        self.mem[current_path[2]] = int(self.mem[current_path[0]] == self.mem[current_path[1]])

        self.ip += param_count

    ### OP CODE = 9
    # ADJUST RELATIVE BASE
    def _adj_rel_base(self, current_path, param_count):
        # increase the relative base by the value of the first parameter
        self.rel_base += self.mem[current_path[0]]

        self.ip += param_count

    ### OP CODE = 99
    # HALT
    def _halt(self, current_path, param_count):
        logging.debug('IP: {} ### HALT ###'.format(self.ip))
        self.done = True

