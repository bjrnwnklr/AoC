# Day 16: Chronal Classification
import re
from collections import defaultdict



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
my_file = open(r'D:\Python\Advent\16.1\input.txt', 'r').readlines()
opcodes = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
results = []
code_results = defaultdict(set)
for i in range((len(my_file) // 4)+1):
    before = [int(x) for x in re.findall(r'\d+', my_file[i*4])]
    instr = [int(x) for x in re.findall(r'\d+', my_file[i*4+1])]
    after = [int(x) for x in re.findall(r'\d+', my_file[i*4+2])]
    op_result = set()
    for f in opcodes:
        if after == f(instr[1], instr[2], instr[3], before):
            op_result.add(f)
    results.append(op_result)
    code_results[instr[0]] = op_result


# count the number of samples with > 3 opcodes
part1 = sum(1 for i in results if len(i) >= 3)
print(part1)

mapping = dict()
found = set()
while len(mapping) < len(opcodes):
    for k in sorted(code_results, key=lambda k: len(code_results[k])):
        
        if k not in mapping and len(code_results[k]) == 1:
            mapping[k] = code_results[k].pop()
            found.add(mapping[k])
            code_results.pop(k)
        else:
            code_results[k] = code_results[k] - found

print(mapping)

##### define registers ######
registers = [0, 0, 0, 0]    
### read in part2 input
for l in  open(r'D:\Python\Advent\16.1\input_2.txt', 'r').readlines():
    f, a, b, c = [int(x) for x in re.findall(r'\d+', l)]
    registers = mapping[f](a, b, c, registers)
    print(registers)

print(registers)
