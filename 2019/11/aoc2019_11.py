# Day 11 - using final version of intcode computer from day 9!

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
        self.mem = defaultdict(int, enumerate(mem))
        
        # input and output queues
        self.in_queue = deque()
        self.out_queue = deque()

        self.opcodes = {
            1: (self.add, 4),
            2: (self.multiply, 4), 
            3: (self.input_f, 2),
            4: (self.output_f, 2),
            5: (self.jump_if_true, 3),
            6: (self.jump_if_false, 3),
            7: (self.less_than, 4),
            8: (self.equals, 4),
            9: (self.adj_rel_base, 2),
            99: (self.halt, 0)}
  

    #### Main run function ####
    def run_intcode(self):
        while (not self.done):
            # get executable intcode method, the number of parameters and the read/write addresses
            int_command, addresses, param_count = self.get_opcode(self.mem[self.ip])

            # execute the opcode
            int_command(addresses, param_count)


    #### Support functions ####
    def get_opcode(self, opcode):
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


    #### OP CODE EXECUTION FUNCTIONS ####

    ### OP CODE = 1
    # ADD
    def add(self, p, param_count):
        # Allow writing in both position and relative mode -- use 3rd parameter
        self.mem[p[2]] = self.mem[p[0]] + self.mem[p[1]]

        self.ip += param_count


    ### OP CODE = 2
    # MULTIPLY
    def multiply(self, p, param_count):
        # Allow writing in both position and relative mode -- use 3rd parameter
        self.mem[p[2]] = self.mem[p[0]] * self.mem[p[1]]

        self.ip += param_count


    ### OP CODE = 3
    # INPUT
    def input_f(self, p, param_count):
        # get input - 
        try:
            s = self.in_queue.popleft()
            self.mem[p[0]] = s
            #logging.debug('IP: {} -- INPUT: popped {}, remaining: {}'.format(self.ip, s, self.in_queue))
        except(IndexError):
            raise InputInterrupt
        else:
            # only advance the instruction pointer if we have taken the input
            self.ip += param_count

    ### OP CODE = 4
    # OUTPUT
    def output_f(self, p, param_count):
        # store message in message stack
        self.out_queue.append(self.mem[p[0]])

        self.ip += param_count

        # pause execution since we passed an output
        raise OutputInterrupt


    ### OP CODE = 5
    # JUMP IF TRUE
    def jump_if_true(self, p, param_count):
        if self.mem[p[0]] != 0:
            self.ip = self.mem[p[1]]
        else:
            self.ip += param_count


    ### OP CODE = 6
    # JUMP IF FALSE
    def jump_if_false(self, p, param_count):
        if self.mem[p[0]] == 0:
            self.ip = self.mem[p[1]]
        else:
            self.ip += param_count


    ### OP CODE = 7
    # LESS THAN
    def less_than(self, p, param_count):
        self.mem[p[2]] = int(self.mem[p[0]] < self.mem[p[1]])

        self.ip += param_count


    ### OP CODE = 8
    # EQUAL
    def equals(self, p, param_count):
        self.mem[p[2]] = int(self.mem[p[0]] == self.mem[p[1]])

        self.ip += param_count

    ### OP CODE = 9
    # ADJUST RELATIVE BASE
    def adj_rel_base(self, p, param_count):
        # increase the relative base by the value of the first parameter
        self.rel_base += self.mem[p[0]]

        self.ip += param_count

    ### OP CODE = 99
    # HALT
    def halt(self, p, param_count):
        logging.debug('IP: {} ### HALT ###'.format(self.ip))
        self.done = True

# dictionary of moves (0: up, 1: right, 2: down, 3: left). Coordinates are (r, c) format
direction = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1)
}

# get new direction - if command = 0, turn left (convert command to -1), if command = 1, turn right
def change_dir(curr, command):
    if command == 0:
        command = -1
    return (curr + command) % 4


#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)


    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')

    # message queue, preconfigured with 0 as input for first amplifier
    msg_stk = deque()

    # initialize the amplifier
    int_comp = Intcode(inp)

    # hull grid - default 0 (black)
    hull = defaultdict(int)
    # starting position = (0, 0)
    pos = (0, 0)
    # starting direction = up (0)
    curr_dir = 0

    # set of painted hull squares
    painted = set()

    # paint / turn toggle - used to determine what output signal means
    # 0 = paint
    # 1 = turn
    out_toggle = 0

    # read initial color and provide as input
    int_comp.in_queue.append(hull[pos])

    # run the amplifier until it halts
    while(not int_comp.done):
        try:
            int_comp.run_intcode()
        except(OutputInterrupt):
            msg = int_comp.out_queue.popleft()
            # paint
            if out_toggle == 0: 
                hull[pos] = msg
                # add pos to painted
                painted.add(pos)
                logging.debug('Painting {} at {}'.format(msg, pos))
            # turn
            elif out_toggle == 1:
                curr_dir = change_dir(curr_dir, msg)
                logging.debug('Turning to {} at {}'.format(curr_dir, pos))
                # and move (only after turn!)
                # move to next square
                pos = (pos[0] + direction[curr_dir][0], pos[1] + direction[curr_dir][1])
                logging.debug('Moving to {}'.format(pos))

                # and read next color square
                int_comp.in_queue.append(hull[pos])
                logging.debug('Read color {} at {}'.format(hull[pos], pos))
        

            # toggle output switch between paint and turn mode
            out_toggle = (out_toggle + 1) % 2
            
    
    logging.info('Part 1 result: {}'.format(len(painted)))
    logging.info('PART 1: End!')


# Part 1: 1771
# Part 2: 

