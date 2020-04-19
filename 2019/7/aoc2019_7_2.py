# Using intcode...

### Part 2

from itertools import permutations
from collections import deque
import logging


class InputInterrupt(Exception):
    pass

class OutputInterrupt(Exception):
    pass


class Amplifier():

    def __init__(self, amp_id, mem):
        # set ip to 0
        self.ip = 0
        
        # set halt parameter
        self.done = False
        self.amp_id = amp_id
                  
        # create a copy of the passed memory
        self.mem = mem[:]
        
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
            99: self.halt}
    

    #### Main run function ####
    def run_intcode(self):
        while (not self.done):
            # get opcode and parameter mode instructions
            param, op = self.get_opcode(self.mem[self.ip])

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

        Return a list of values for the memory retrieved from parameters.
        """
        mems = []
        # go through each parameter and retrieve value based on parameter mode
        for i in range(1, param_count + 1):
            p_mode = int(param[-i]) # -i since param mode goes from right to left
            if p_mode == 1:         # immediate mode
                m = self.mem[self.ip + i]
            else:                   # position mode
                m = self.mem[self.mem[self.ip + i]]
            mems.append(m)

        return mems


    #### OP CODE EXECUTION FUNCTIONS ####

    ### OP CODE = 1
    # ADD
    def add(self, param):
        param_count = 3
        p = self.get_param(param_count, param)

        # target is always in position mode, so don't use the value retrieved and write directly to mem
        self.mem[self.mem[self.ip+3]] = p[0] + p[1]

        self.ip += param_count + 1


    ### OP CODE = 2
    # MULTIPLY
    def multiply(self, param):
        param_count = 3
        p = self.get_param(param_count, param)

        # target is always in position mode, so don't use the value retrieved and write directly to mem
        self.mem[self.mem[self.ip+3]] = p[0] * p[1]

        self.ip += param_count + 1


    ### OP CODE = 3
    # INPUT
    def input_f(self, param):
        param_count = 1

        # get input - 
        try:
            s = self.in_queue.popleft()
            self.mem[self.mem[self.ip+1]] = s
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
        self.out_queue.append(p[0])

        logging.debug('IP: {} -- OUTPUT: {}'.format(self.ip, self.out_queue))

        self.ip += param_count + 1

        # pause execution since we passed an output
        raise OutputInterrupt


    ### OP CODE = 5
    # JUMP IF TRUE
    def jump_if_true(self, param):
        param_count = 2
        p = self.get_param(param_count, param)

        #print('IP: {} __ jump-if-true: {}'.format(ip, mems[0]))

        if p[0] != 0:
            self.ip = p[1]
        else:
            self.ip += param_count + 1


    ### OP CODE = 6
    # JUMP IF FALSE
    def jump_if_false(self, param):
        param_count = 2
        p = self.get_param(param_count, param)

        #print('IP: {} __ jump-if-false: {}'.format(ip, mems[0]))

        if p[0] == 0:
            self.ip = p[1]
        else:
            self.ip += param_count + 1


    ### OP CODE = 7
    # LESS THAN
    def less_than(self, param):
        param_count = 3
        p = self.get_param(param_count, param)

        #print('IP: {} __ less-than: {} < {}'.format(ip, mems[0], mems[1]))

        self.mem[self.mem[self.ip+3]] = int(p[0] < p[1])

        self.ip += param_count + 1


    ### OP CODE = 8
    # EQUAL
    def equals(self, param):
        param_count = 3
        p = self.get_param(param_count, param)

        #print('IP: {} __ equal: {} < {}'.format(ip, mems[0], mems[1]))

        self.mem[self.mem[self.ip+3]] = int(p[0] == p[1])

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

    # dictionary with results - store output value for each phase permutation
    results = dict()

    logging.info('PART 1: Starting!')

    for p in permutations(range(5)):
        # take a copy of the phases to store
        temp_phase = p[:]
        # create a list (permutations gives you a tuple)
        phases = list(p)

        # message queue, preconfigured with 0 as input for first amplifier
        msg_stk = deque([0])

        # run the main amplifier loop
        for i, p in enumerate(phases):
            # initialize the amplifier
            amp = Amplifier(i, inp)
            # add the phase to the amplifier
            amp.in_queue.append(p)
            # add the output from the previous amp to the amplifier in_queue
            amp.in_queue.append(msg_stk.pop())
            # run the amplifier until it halts
            while(not amp.done):
                try:
                    amp.run_intcode()
                except(OutputInterrupt):
                    pass
            # retrieve the output and add to msg_queue
            msg_stk.append(amp.out_queue.popleft())

        # retrieve result
        res = msg_stk[0]

        #print('Result for {}: {}'.format(temp_phase, res))
        results[temp_phase] = res

    # get max from dictionary
    max_key = max(results, key=results.get)
    print('-- Max phase: {}, output: {}'.format(max_key, results[max_key]))

    logging.info('PART 1: End!')

    ## part 1 result: 273814

    ##### Part 2

    # dictionary with results - store output value for each phase permutation
    results = dict()

    logging.info('PART 2: Starting!')

    for p in permutations(range(5, 10)):
        # take a copy of the phases to store
        temp_phase = p[:]
        # create a list (permutations gives you a tuple)
        phases = list(p)

        # message queue, preconfigured with 0 as input for first amplifier
        msg_stk = deque([0])

        # amplifier list
        amps_queue = deque()

        # initialize amplifier queue with phases
        for i, p in enumerate(phases):
            amp = Amplifier(i, inp)
            amp.in_queue.append(p)
            amps_queue.append(amp)
            
        while amps_queue:  
            # pop the first amp
            amp = amps_queue.popleft()
            
            logging.debug('Amp {} running'.format(amp.amp_id))          
            
            # add the output from the previous amp to the amplifier in_queue
            amp.in_queue.append(msg_stk.pop())
            # run the amplifier until it requests more input - fill the output queue until input requested
            # stop when input requested and move on to next amp.
            while(not amp.done):
                try:
                    amp.run_intcode()
                except(OutputInterrupt):
                    msg_stk.append(amp.out_queue.popleft())
                    continue # the continue here ensures the amp runs to the next input point or halts
                except(InputInterrupt):
                    break # if we need input, break and stop, move to next amp

            logging.debug('Amp {} stopping'.format(amp.amp_id))   

            # add amp back into queue if not done
            if not amp.done:
                amps_queue.append(amp)
            else:
                logging.debug('Amp {} taken out of queue.'.format(amp.amp_id))
              

        # retrieve result
        res = msg_stk[0]

        #print('Result for {}: {}'.format(temp_phase, res))
        results[temp_phase] = res

    # get max from dictionary
    max_key = max(results, key=results.get)
    print('-- Max phase: {}, output: {}'.format(max_key, results[max_key]))

    logging.info('PART 2: End!')

    # part 2 solution: 34579864