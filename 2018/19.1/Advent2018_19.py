#### Day 19: go with the flow

##### define opcodes #######

### Addition
def addr(a, b, c, regs):
    reg = regs[:]
    reg[c] = reg[a] + reg[b]
    return reg

def addi(a, b, c, regs):
    reg = regs[:]
    reg[c] = reg[a] + b
    return reg

### Multiplication
def mulr(a, b, c, regs):
    reg = regs[:]
    reg[c] = reg[a] * reg[b]
    return reg

def muli(a, b, c, regs):
    reg = regs[:]
    reg[c] = reg[a] * b
    return reg

### Bitwise AND
def banr(a, b, c, regs):
    reg = regs[:]
    reg[c] = reg[a] & reg[b]
    return reg

def bani(a, b, c, regs):
    reg = regs[:]
    reg[c] = reg[a] & b
    return reg

### Bitwise OR
def borr(a, b, c, regs):
    reg = regs[:]
    reg[c] = reg[a] | reg[b]
    return reg

def bori(a, b, c, regs):
    reg = regs[:]
    reg[c] = reg[a] | b
    return reg

### Assignment
def setr(a, b, c, regs):
    reg = regs[:]
    reg[c] = reg[a]
    return reg

def seti(a, b, c, regs):
    reg = regs[:]
    reg[c] = a
    return reg

### Greater-than testing
def gtir(a, b, c, regs):
    reg = regs[:]
    if a > reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0
    return reg

def gtri(a, b, c, regs):
    reg = regs[:]
    if reg[a] > b:
        reg[c] = 1
    else:
        reg[c] = 0
    return reg

def gtrr(a, b, c, regs):
    reg = regs[:]
    if reg[a] > reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0
    return reg

### Equality testing
def eqir(a, b, c, regs):
    reg = regs[:]
    if a == reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0
    return reg

def eqri(a, b, c, regs):
    reg = regs[:]
    if reg[a] == b:
        reg[c] = 1
    else:
        reg[c] = 0
    return reg

def eqrr(a, b, c, regs):
    reg = regs[:]
    if reg[a] == reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0
    return reg





#### read the file, part 1 only
my_file = open(r'input.txt', 'r')
# read the instruction pointer register first
ipr = int(my_file.readline()[4])
# read in the individual instructions
instructions = []
for l in my_file:
    instr, a, b, c = l.rstrip('\n').split(' ')
    instructions.append((instr, int(a), int(b), int(c)))



##### define registers ######
# the code finds prime factors for the number in register #1 (998)
# then adds the prime factors (including 1 and 998 itself) in reg #0
# once that is completed, it ends the program
# this register state is before the last iteration where 998 itself is added
# 502 = 1 + 2 + 499 (prime factors of 998)
# part 1 answer is 1500 (1 + 2 + 499 + 998)
registers = [502, 998, 998, 1, 998, 7]
ip = 7 # instruction pointer starts at 0

# go through instructions
while ip < len(instructions):
    
    registers[ipr] = ip   # write the instruction pointer to the reg

    pr_line = 'ip=%d ' % ip
    pr_line += str(registers)

    f, a, b, c = instructions[ip]
    pr_line += ' %s %d %d %d ' % (f, a, b, c)

    f = eval(f)
    registers = f(a, b, c, registers)
    pr_line += str(registers)

    print(pr_line)
    
    ip = registers[ipr] + 1



print(registers)
