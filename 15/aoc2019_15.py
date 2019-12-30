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
#  clockwise movement: north (1), east (4), south (2), west (3)
# grid is x, y with positive x to the east (right) and positive y to the south (down)
n_coords = [((0, -1), 1), ((1, 0), 4), ((0, 1), 2), ((-1, 0), 3)]

# clockwise direction

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

    logging.debug('Current grid dimensions: {} * {}, total size {}'.format(max_x + 1 - min_x, max_y + 1 - min_y, len(grid)))
    logging.debug('Droid is at {}'.format(droid))

    for y in range(min_y, max_y + 1):
        line = ''.join('D' if droid == (x, y) else grid[(x, y)] for x in range(min_x, max_x + 1))
        print(line) 


def intcode_move(int_comp, dir):
    int_comp.in_queue.append(dir) 
    # logging.debug('Input queue: {}'.format(int_comp.in_queue))
    while(not int_comp.done):   
        try:
            int_comp.run_intcode()
        except(InputInterrupt):
            # do nothing
            pass
        except(OutputInterrupt):
            # read output and return output
            # logging.debug('Output queue: {}'.format(int_comp.out_queue))
            return int_comp.out_queue.popleft()


    
#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)


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
    start = (0, 0)
    droid = start
    feel_dir = 2 # start by feeling the wall to the south and going east (right wall hugging)
    move_dir = 1
    oxygen_pos = tuple()
    found = False
    prev_grid_size = -10
    seen = set()


    # initialize the intcode machine
    int_comp = Intcode(inp)

    # implement wall hugging algorithm
    # 1) feel to the right
    # 2a) if wall, move ahead (dir - 1)
    # 2b) if no wall, you have moved into empty space, then turn right
    # 3) repeat
    while(len(seen) < 1653):

        # feel the wall to the right
        feel_wall = n_coords[feel_dir]
        next_pos = (droid[0] + feel_wall[0][0], droid[1] + feel_wall[0][1])
        status_code = intcode_move(int_comp, feel_wall[1])
        grid[next_pos] = status_to_grid[status_code]
        seen.add(next_pos)

        # if we feel a wall, continue moving ahead without turning (move into direction - 1)
        if status_code == 0:
            # logging.debug('At {}, wall to the right, trying to move ahead.'.format(next_pos))
            # we have a wall to the right, now try moving ahead
            move_pos = n_coords[move_dir]
            next_pos = (droid[0] + move_pos[0][0], droid[1] + move_pos[0][1])
            status_code = intcode_move(int_comp, move_pos[1])
            grid[next_pos] = status_to_grid[status_code]
            seen.add(next_pos)
            
            # if we hit a wall turn counter clockwise to keep the wall to the right
            if status_code == 0:
                # logging.debug('\tHit a wall ahead at {}, turning counterclockwise from {}.'.format(next_pos, move_dir))
                feel_dir = (feel_dir - 1) % 4
                move_dir = (move_dir - 1) % 4
            else: 
                # logging.debug('\tMoved ahead to {} successsfully.'.format(next_pos))
                # we hit no wall so can move straight ahead
                droid = next_pos   
                if status_code == 2:
                    found = True
                    oxygen_pos = droid 
        else:
            # we have no wall to the right, so turn right (we have already moved into the empty space)
            # logging.debug('Found no wall to the right, so moved to {} and now turning clockwise from {}'.format(next_pos, move_dir))
            feel_dir = (feel_dir + 1) % 4
            move_dir = (move_dir + 1) % 4
            droid = next_pos
            if status_code == 2:
                found = True
                oxygen_pos = droid

        # draw_grid(grid, droid)


            
    # we get to here if the BFS finishes
    # 
    logging.info('BFS ended, position of oxygen system is: {}'.format(oxygen_pos))    

    draw_grid(grid, droid)    
            
        
    logging.info('PART 1: End!')


# part 1: 
# part 2: 