# Day 13 - game with intcode!

from collections import deque, defaultdict
import logging
import math


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
        s = self.in_queue.popleft()
        self.mem[p[0]] = s
        
        self.ip += param_count

        raise InputInterrupt

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


def process_game_output(q, grid, rounds):

    logging.debug('Round {}: output queue length: {}'.format(rounds, len(q)))
    logging.debug('Queue: {}'.format(q))

    # default move returned is 0 (stay put)
    move = 0

    # now process the output queue
    while q:
        # get next three elements
        x, y, tile = (q.popleft() for _ in range(3))
        
        # check for score display
        if (x, y) == (-1, 0):
            logging.info('Score after {} rounds: {}'.format(rounds, tile))
        # count the block tiles (tile type #2)
        # if ball moves, move the paddle in the same direction
        elif tile == 4:
            # need position of paddle and position of ball here
        else:
            grid[(x, y)] = tile
        
    return grid

tiles = {
    0: ' ',
    1: '#',
    2: '%',
    3: '=',
    4: '@'
}

def draw_game(grid):
    # grid is 42 wide (x) and 22 tall (y)
    for y in range(23):
        print(''.join([tiles[grid[(x, y)]] for x in range(43)]))




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

    # part 2: set mem 0 to 2
    inp[0] = 2

    # initialize the amplifier
    int_comp = Intcode(inp)

    # the grid
    grid = dict()

    # try some initial input
    joystick = [0, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 

    for x in joystick:
        int_comp.in_queue.append(x)

    # count how many rounds we play
    rounds = 0

    # run the amplifier until it halts
    while(not int_comp.done):
        try:
            int_comp.run_intcode()
        except(InputInterrupt):
            grid = process_game_output(int_comp.out_queue, grid, rounds)
            draw_game(grid)
            rounds += 1
        except(OutputInterrupt):
            #logging.info('Output: {}'.format(int_comp.out_queue[-1]))
            pass
            # let the output queue fill up until the game finishes

    
        


    #logging.info('Part 1 - number of block tiles: {}'.format(blocks))
    logging.info('PART 1: End!')


# part 1: 363 block tiles!

# Part 1: 2682107844
# Part 2: 34738

