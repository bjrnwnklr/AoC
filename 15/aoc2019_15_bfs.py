# Day 15 - path finding with intcode!

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


    def dump_state(self):
        return (self.mem.copy(), self.ip, self.rel_base)

    def load_state(self, intcode_state):
        self.mem, self.ip, self.rel_base = intcode_state

    #### OP CODE EXECUTION FUNCTIONS ####

    ### OP CODE = 1
    # ADD
    def add(self, current_path, param_count):
        # Allow writing in both position and relative mode -- use 3rd parameter
        self.mem[current_path[2]] = self.mem[current_path[0]] + self.mem[current_path[1]]

        self.ip += param_count


    ### OP CODE = 2
    # MULTIPLY
    def multiply(self, current_path, param_count):
        # Allow writing in both position and relative mode -- use 3rd parameter
        self.mem[current_path[2]] = self.mem[current_path[0]] * self.mem[current_path[1]]

        self.ip += param_count


    ### OP CODE = 3
    # INPUT
    def input_f(self, current_path, param_count):
        # get input - 
        s = self.in_queue.popleft()
        self.mem[current_path[0]] = s
        
        self.ip += param_count

        raise InputInterrupt

    ### OP CODE = 4
    # OUTPUT
    def output_f(self, current_path, param_count):
        # store message in message stack
        self.out_queue.append(self.mem[current_path[0]])

        self.ip += param_count

        # pause execution since we passed an output
        raise OutputInterrupt


    ### OP CODE = 5
    # JUMP IF TRUE
    def jump_if_true(self, current_path, param_count):
        if self.mem[current_path[0]] != 0:
            self.ip = self.mem[current_path[1]]
        else:
            self.ip += param_count


    ### OP CODE = 6
    # JUMP IF FALSE
    def jump_if_false(self, current_path, param_count):
        if self.mem[current_path[0]] == 0:
            self.ip = self.mem[current_path[1]]
        else:
            self.ip += param_count


    ### OP CODE = 7
    # LESS THAN
    def less_than(self, current_path, param_count):
        self.mem[current_path[2]] = int(self.mem[current_path[0]] < self.mem[current_path[1]])

        self.ip += param_count


    ### OP CODE = 8
    # EQUAL
    def equals(self, current_path, param_count):
        self.mem[current_path[2]] = int(self.mem[current_path[0]] == self.mem[current_path[1]])

        self.ip += param_count

    ### OP CODE = 9
    # ADJUST RELATIVE BASE
    def adj_rel_base(self, current_path, param_count):
        # increase the relative base by the value of the first parameter
        self.rel_base += self.mem[current_path[0]]

        self.ip += param_count

    ### OP CODE = 99
    # HALT
    def halt(self, current_path, param_count):
        logging.debug('IP: {} ### HALT ###'.format(self.ip))
        self.done = True


################ global constants #######################
#  north (1), south (2), west (3), and east (4)
# grid is x, y with positive x to the east (right) and positive y to the south (down)
n_coords = [(0, -1), (0, 1), (-1, 0), (1, 0)]
# n_coords = [(0, -1), (0, 1), (-1, 0), (1, 0)]


status_to_grid = {
    0: '#', # wall
    1: '.', # found a moveable space
    2: '@'  # found the oxygen system
}


def draw_grid(grid, droid):
    # now dump the default grid into a matrix to display
    # find the min / max coordinates
    keys = grid.keys()
    min_y = min(keys, key=lambda x: x[1])[1]
    max_y = max(keys, key=lambda x: x[1])[1]
    min_x = min(keys, key=lambda x: x[0])[0]
    max_x = max(keys, key=lambda x: x[0])[0]

    for y in range(min_y, max_y + 1):
        line = ''.join('D' if droid == (x, y) else grid[(x, y)] for x in range(min_x, max_x + 1))
        print(line) 


def intcode_move(droid_copy, dir):
    int_comp = droid_copy
    int_comp.in_queue.append(dir) 
    while(not int_comp.done):   
        try:
            int_comp.run_intcode()
        except(InputInterrupt):
            # do nothing
            pass
        except(OutputInterrupt):
            # read output and return output
            output = int_comp.out_queue.popleft()
            break

    return output


    
#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(level=logging.DEBUG, filename='droid.log')


    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    logging.info('PART 1: Starting!')

    # the playing field grid
    # grid is represented by 
    # ' ' = empty space (not explored)
    # '#' = wall
    # '.' = traversable space
    grid = defaultdict(lambda: ' ')
    droid = (0, 0)
    grid[droid] = '.'
    oxygen_pos = tuple()


    # initialize the intcode machine
    int_comp = Intcode(inp)

    # BFS stuff
    # q contains the following:
    # 0: current position (x, y) tuple
    # 1: current path (list)
    # 2: memory dump of the intcode program
    # 3: instruction pointer of the intcode program
    # 4: relative base value of the intcode program
    q = deque([(droid, [])])
    droid_reg = {droid: int_comp}
    seen = set()
    path = defaultdict(list)

    # run BFS until we have explored every grid cell
    while(q):

         # removes element from the right side of the queue
        current_pos, current_path = q.pop()

        # once at current_pos, find all valid neighbours
        for i, n in enumerate(n_coords):
            v_next = (current_pos[0] + n[0], current_pos[1] + n[1])
            dir = i + 1
            if (v_next not in seen):

                # explore the new space - try moving to it!
                # ... send move instruction to new space
                droid_copy = deepcopy(droid_reg[current_pos])
                status_code = intcode_move(droid_copy, dir)
                grid[v_next] = status_to_grid[status_code]
                seen.add(v_next)
                droid_reg[v_next] = droid_copy

                # if space is not a wall, add to queue. We already moved to the new place by giving the input instruction.
                # set the path to this new square
                if status_code != 0:
                    droid = v_next
                    path[v_next] = current_path + [v_next]
                    q.appendleft((v_next, current_path + [v_next]))
                    # logging.debug('Appended {}, q: {}'.format(v_next, q))
                    # check if we found the oxygen thingy and store the position
                    if status_code == 2:
                        oxygen_pos = v_next
                        logging.info('Found the oxygen system at {}!!'.format(oxygen_pos))
        
    # we get to here if the BFS finishes
    # 
    logging.info('BFS ended, position of oxygen system is: {}'.format(oxygen_pos))    

    draw_grid(grid, droid)    
            
        
    logging.info('PART 1: End!')


# part 1: 
# part 2: 