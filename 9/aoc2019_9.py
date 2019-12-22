# Day 9 - final version of intcode computer!

from collections import deque, defaultdict
import logging


class InputInterrupt(Exception):
    pass

class OutputInterrupt(Exception):
    pass


class Intcode():

    def __init__(self, mem, amp_id=1):
        # set ip to 0
        self.ip = 0

        # set relative base to 0
        self.rel_base = 0
        
        # set halt parameter
        self.done = False
        self.amp_id = amp_id
                  
        # create a defaultdict of the memory values to allow for positive addresses with 0 value
        self.mem = defaultdict(int)
        for i, m in enumerate(mem):
            self.mem[i] = m
        
        # input and output queues
        self.in_queue = deque()
        self.out_queue = deque()

        self.opcodes = {
            1: self.add, 
            2: self.multiply, 
            3: self.input_f, 
            4: self.output_f, 
            5: self.jump_if_true, 
            6: self.jump_if_false, 
            7: self.less_than,
            8: self.equals,
            9: self.adj_rel_base,
            99: self.halt}
    

    #### Main run function ####
    def run_intcode(self):
        while (not self.done):
            # get opcode and parameter mode instructions
            param, op = self.get_opcode(self.mem[self.ip])

            logging.debug('IP {}: Op {}, params {}, rel_base {}'.format(self.ip, op, param, self.rel_base))
            logging.debug('\tMem: {}'.format(self.mem))

            # execute the opcode
            self.opcodes[op](param)


    #### Support functions ####
    def get_opcode(self, opcode):
        # pad opcode to 6 digits with zeroes
        ops = str(opcode).zfill(6)
        # decode opcode - get last two digits, rest are parameter modes
        op = int(ops[-2:])
        param = ops[:-2]
        
        return param, op

    def get_param(self, param_count, param):
        """
        Get the values for each paramater, based on parameter mode.
        Supports unlimited positive memory addresses beyond the memory initially provided (all values start at 0). 
        Trying to access negative memory produces an Exception.

        Return a list of values for the memory retrieved from parameters
        """
        addresses = []
        # go through each parameter and retrieve value based on parameter mode
        for i in range(1, param_count + 1):
            p_mode = int(param[-i]) # -i since param mode goes from right to left
            
            # parameter modes:
            # 1 = immediate mode
            if p_mode == 1:
                addr = self.ip + i

            # 0 = position mode
            elif p_mode == 0: 
                addr = self.mem[self.ip + i]
                # check if we try to access negative memory address
                if addr < 0:
                    raise ValueError('Trying to access negative memory at {}!'.format(addr))

            # 2 = relative mode
            elif p_mode == 2:
                addr = self.mem[self.ip + i] + self.rel_base
                # check if we try to access negative memory address
                if addr < 0:
                    raise ValueError('Trying to access negative memory at {}!'.format(addr))
            
            addresses.append(addr)

        return addresses


    #### OP CODE EXECUTION FUNCTIONS ####

    ### OP CODE = 1
    # ADD
    def add(self, param):
        param_count = 3
        p = self.get_param(param_count, param)

        # Allow writing in both position and relative mode -- use 3rd parameter
        self.mem[p[2]] = self.mem[p[0]] + self.mem[p[1]]

        self.ip += param_count + 1


    ### OP CODE = 2
    # MULTIPLY
    def multiply(self, param):
        param_count = 3
        p = self.get_param(param_count, param)

        # Allow writing in both position and relative mode -- use 3rd parameter
        self.mem[p[2]] = self.mem[p[0]] * self.mem[p[1]]

        self.ip += param_count + 1


    ### OP CODE = 3
    # INPUT
    def input_f(self, param):
        param_count = 1
        p = self.get_param(param_count, param)

        # get input - 
        try:
            s = self.in_queue.popleft()
            self.mem[p[0]] = s
            logging.debug('IP: {} -- INPUT: popped {}, remaining: {}'.format(self.ip, s, self.in_queue))
        except(IndexError):
            raise InputInterrupt
        else:
            # only advance the instruction pointer if we haven't taken the input
            self.ip += param_count + 1

    ### OP CODE = 4
    # OUTPUT
    def output_f(self, param):
        param_count = 1
        p = self.get_param(param_count, param)

        # store message in message stack
        self.out_queue.append(self.mem[p[0]])

        self.ip += param_count + 1

        # pause execution since we passed an output
        raise OutputInterrupt


    ### OP CODE = 5
    # JUMP IF TRUE
    def jump_if_true(self, param):
        param_count = 2
        p = self.get_param(param_count, param)

        if self.mem[p[0]] != 0:
            self.ip = self.mem[p[1]]
        else:
            self.ip += param_count + 1


    ### OP CODE = 6
    # JUMP IF FALSE
    def jump_if_false(self, param):
        param_count = 2
        p = self.get_param(param_count, param)

        if self.mem[p[0]] == 0:
            self.ip = self.mem[p[1]]
        else:
            self.ip += param_count + 1


    ### OP CODE = 7
    # LESS THAN
    def less_than(self, param):
        param_count = 3
        p = self.get_param(param_count, param)

        self.mem[p[2]] = int(self.mem[p[0]] < self.mem[p[1]])

        self.ip += param_count + 1


    ### OP CODE = 8
    # EQUAL
    def equals(self, param):
        param_count = 3
        p = self.get_param(param_count, param)

        self.mem[p[2]] = int(self.mem[p[0]] == self.mem[p[1]])

        self.ip += param_count + 1

    ### OP CODE = 9
    # ADJUST RELATIVE BASE
    def adj_rel_base(self, param):
        param_count = 1
        p = self.get_param(param_count, param)

        # increase the relative base by the value of the first parameter
        self.rel_base += self.mem[p[0]]

        self.ip += param_count + 1

    ### OP CODE = 99
    # HALT
    def halt(self, param):
        logging.debug('IP: {} ### HALT ###'.format(self.ip))
        self.done = True





#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)


    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')

    # message queue, preconfigured with 0 as input for first amplifier
    msg_stk = deque()

    # initialize the amplifier
    int_comp = Intcode(inp)

    # provide 1 as input for test mode
    # provide 2 as input for BOOST mode
    init_inp = 2
    
    int_comp.in_queue.append(init_inp)

    # run the amplifier until it halts
    while(not int_comp.done):
        try:
            int_comp.run_intcode()
        except(OutputInterrupt):
            msg = int_comp.out_queue.popleft()
            msg_stk.append(msg)
            logging.info('Output: {}'.format(msg))

    # retrieve result (last entry in out_queue)
    res = msg_stk[-1]

    logging.info('Part 1 result: {}'.format(res))
    logging.info('PART 1: End!')


# Part 1: 2682107844
# Part 2: 34738

