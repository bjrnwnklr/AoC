from collections import defaultdict
import re


def generate_bitmask(mask):
    set_1 = 0b0
    set_0 = 0b0

    for i, c in enumerate(mask[::-1]):
        if c == '1':
            # set the ith bit to 1 in the set_1 mask
            set_1 |= 1 << i
        elif c == '0':
            # set the ith bit to 1 in the set_0 mask
            set_0 |= 1 << i

    return set_0, set_1


def apply_bitmask(val, set_0, set_1):
    # apply set_0 mask, setting bits to 0
    val &= ~ set_0
    # apply set_1 mask, setting bits to 1
    val |= set_1
    return val


# f_name = 'ex1.txt'
f_name = 'input.txt'

# initialize everything
mem = defaultdict(int)
set_0 = 0b0
set_1 = 0b0

with open(f_name, 'r') as f:
    for line in f.readlines():
        if 'mask' in line:
            # mask line - generate a new bitmask
            mask = line.strip('\n').split(' = ')[-1]
            set_0, set_1 = generate_bitmask(mask)
        else:
            # setting a memory value - retrieve mem pos and value and apply bitmask, then store in mem
            pos, val = tuple(map(int, re.findall(r'(\d+)', line)))
            mem[pos] = apply_bitmask(val, set_0, set_1)

# Now sum up all the values
part1 = sum(mem.values())
print(f'Part 1: {part1}')

# Part 1: 14954914379452
