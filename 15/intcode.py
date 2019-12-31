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
        s = self.in_queue.popleft()
        self.mem[current_path[0]] = s
        
        self.ip += param_count

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


################ global constants #######################
#  north (1), south (2), west (3), and east (4)
# grid is x, y with positive x to the east (right) and positive y to the south (down)
n_coords = [(0, -1), (0, 1), (-1, 0), (1, 0)]


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
        line = []
        for x in range(min_x, max_x + 1):
            c = grid[(x, y)]
            if (x, y) == droid:
                c = 'D'
            elif (x, y) == (0, 0):
                c = 'S'
            line.append(c)
        print(''.join(line))

def draw_path(grid, start, droid, path):
    # now dump the default grid into a matrix to display
    # find the min / max coordinates
    keys = grid.keys()
    min_y = min(keys, key=lambda x: x[1])[1]
    max_y = max(keys, key=lambda x: x[1])[1]
    min_x = min(keys, key=lambda x: x[0])[0]
    max_x = max(keys, key=lambda x: x[0])[0]

    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            c = grid[(x, y)]
            if (x, y) == droid:
                c = 'D'
            elif (x, y) == start:
                c = 'S'
            elif (x, y) in path:
                c = '*'
            line.append(c)
        print(''.join(line))




    
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
    droid = start = (0, 0)
    grid[droid] = '.'
    oxygen_pos = tuple()
    # graph for part 2
    graph = defaultdict(set)

    # initialize the intcode machine
    int_comp = Intcode(inp)

    # BFS stuff
    # q contains the following:
    # 0: current position (x, y) tuple
    # 1: current path (list)
    q = deque([(droid, [])])
    # droid_reg stores the state of the intcode computer at a coordinate - to retrieve when backtracking
    droid_reg = {droid: int_comp}
    # path stores the path to each individual point in the grid as explored by BFS
    path = defaultdict(list)

    # run BFS until we have explored every grid cell
    while(q):

         # removes element from the right side of the queue
        current_pos, current_path = q.pop()

        # once at current_pos, find all valid neighbours
        for direction, n in enumerate(n_coords, start=1):
            v_next = (current_pos[0] + n[0], current_pos[1] + n[1])
            # direction = i + 1
            if (v_next not in droid_reg):

                # explore the new space - try moving to it. 
                # 1) Retrieve a copy of the intcode computer at the current position
                # 2) Try moving to the new coordinate
                # 3) update status of the new coordinate in the grid
                # 4) store the updated droid at the new location
                droid_copy = droid_reg[current_pos].clone()
                status_code = droid_copy.run_input_output(direction)
                grid[v_next] = status_to_grid[status_code]
                droid_reg[v_next] = droid_copy

                # if space is not a wall, add to queue. We already moved to the new place by giving the input instruction.
                # set the path to this new square
                if status_code != 0:
                    droid = v_next
                    path[v_next] = current_path + [v_next]
                    q.appendleft((v_next, current_path + [v_next]))
                    # for part 2 - generate a graph with neighbors
                    graph[current_pos].add(v_next)
                    graph[v_next].add(current_pos)
                    # check if we found the oxygen thingy and store the position
                    if status_code == 2:
                        oxygen_pos = v_next
                        logging.info('Found the oxygen system at {}!!'.format(oxygen_pos))
        
    # we get to here if the BFS finishes
    draw_path(grid, start, droid, path[oxygen_pos][:-1])    

    logging.info('BFS ended, path from {} to oxygen system is: {}'.format(start, path[oxygen_pos]))    
    logging.info('Part 1: shortest path to oxygen system is {} steps long'.format(len(path[oxygen_pos])))
    logging.info('PART 1: End!')


    ##### Part 2
    # 
    # Do a BFS using the graph, starting from the oxygen source
    # - valid neighbors are contained in the graph dictionary

    q = deque([(oxygen_pos, [])])
    oxygen_bfs_seen = set()
    oxygen_bfs_path = defaultdict(list)

    while(q):
        current_pos, current_path = q.pop()

        # go through neighbors using the graph
        for neighbor in graph[current_pos]:
            if neighbor not in oxygen_bfs_seen:
                oxygen_bfs_seen.add(neighbor)
                oxygen_bfs_path[neighbor] = current_path + [neighbor]
                q.appendleft((neighbor, current_path + [neighbor]))

    logging.info('Oxygen BFS ended!')

    # get the longest path length from the oxygen source
    furthest_from_oxygen = max(oxygen_bfs_path, key=lambda x: len(oxygen_bfs_path[x]))    
    logging.info('Longest distance from oxygen source is {} at {} steps'.format(
        furthest_from_oxygen, 
        len(oxygen_bfs_path[furthest_from_oxygen])
        ))

    draw_path(grid, oxygen_pos, furthest_from_oxygen, oxygen_bfs_path[furthest_from_oxygen][:-1])

# part 1: 262 steps
# part 2: 314 minutes