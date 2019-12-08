# Using intcode...

### Part 1

from itertools import permutations

class Amplifier():

    def __init__(self, amp_id, phase, mem, msg_stk):
        # set ip to 0
        self.ip = 0
        # set halt parameter
        self.do_halt = False
        self.amp_id = amp_id
        # assign initial phase value and set the init flag to True 
        # (signals that we need to read the phase when getting to the first input_f command)
        self.phase = phase
        self.init_flag = True
        # create a copy of the passed memory
        self.mem = mem[:]
        # use a reference to the msg_stk
        self.msg_stk = msg_stk

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
        while (not self.do_halt):
            # get opcode and parameter mode instructions
            param, op = self.get_opcode(self.mem[self.ip])

            # execute the opcode
            self.opcodes[op](param)


    #### Support functions ####
    def get_opcode(self, opcode):
        ops = str(opcode).zfill(6)
        # decode opcode - get last two digits
        op = int(ops[-2:])
        param = ops[:-2]
        
        return param, op

    def get_param(self, param_count, param):
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
        # - get the phase if this is the first time (use self.init_flag to determine)
        # pop the first element from the phases input
        if self.init_flag:
            s = self.phase
            self.init_flag = False
        else:
            s = self.msg_stk.pop()
        #print('IP: {} -- INPUT: popped {}, remaining: {}'.format(ip, s, self.msg_stk))

        self.mem[self.mem[self.ip+1]] = s

        self.ip += param_count + 1


    ### OP CODE = 4
    # OUTPUT
    def output_f(self, param):
        param_count = 1
        p = self.get_param(param_count, param)

        # store message in message stack
        self.msg_stk.append(p[0])

        #print('IP: {} -- OUTPUT: {}, phases: {}'.format(ip, out, args[0]))

        ## TO DO: This needs to change for part 2 - set a flag that we have passed on an output
        self.ip += param_count + 1


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
        #print('IP: {} ### HALT ###'.format(ip))
        self.do_halt = True





#### main program ####

if __name__ == '__main__':
    # read input
    f_name = 'input.txt'
    inp = list(map(int, open(f_name).readline().split(',')))

    print('PART 1: Starting!')

    results = dict()

    for p in permutations(range(5)):
        # take a copy of the phases to store
        temp_phase = p[:]

        # create a list (permutations gives you a tuple)
        phases = list(p)

        # initialize message stack
        msg_stk = [0]

        for i, p in enumerate(phases):
            amp = Amplifier(i, p, inp, msg_stk)
            amp.run_intcode()

        # retrieve result
        res = msg_stk[0]

        print('Result for {}: {}'.format(temp_phase, res))
        results[temp_phase] = res

    # get max from dictionary
    max_key = max(results, key=results.get)
    print('-- Max phase: {}, output: {}'.format(max_key, results[max_key]))

    print('PART 1: End!')