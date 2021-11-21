from collections import defaultdict
import re
from itertools import product


def generate_bitmask(mask):
    set_1 = 0b0
    set_0 = 0b0
    floating = []

    for i, c in enumerate(mask[::-1]):
        if c == '1':
            # for part 2, we don't do anything if a 0 is found
            # set the ith bit to 1 in the set_1 mask
            set_1 |= 1 << i
        elif c == 'X':
            # found a floating bit, record its index
            floating.append(i)

    return set_0, set_1, floating


def get_combinations(n):
    return product([0, 1], repeat=n)


def apply_bitmask(val, set_0, set_1, floating):
    mem_addresses = []
    # now apply all floating bit and create new addresses
    combinations = get_combinations(len(floating))
    for c in combinations:
        temp_val = val
        temp_set_0 = set_0
        temp_set_1 = set_1
        for b, i in zip(c, floating):
            if b == 0:
                temp_set_0 |= 1 << i
            else:
                temp_set_1 |= 1 << i

            # apply set_0 mask, setting bits to 0
            temp_val &= ~ temp_set_0
            # apply set_1 mask, setting bits to 1
            temp_val |= temp_set_1

        mem_addresses.append(temp_val)

    return mem_addresses


# f_name = 'ex2.txt'
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
            set_0, set_1, floating = generate_bitmask(mask)
        else:
            # setting a memory value - retrieve mem pos and value and apply bitmask, then store in mem
            pos, val = tuple(map(int, re.findall(r'(\d+)', line)))
            # print(f'pos {pos:08b} {pos}')
            mem_addresses = apply_bitmask(pos, set_0, set_1, floating)
            for m in mem_addresses:
                # print(f'mem {m:08b} {m}: {val}')
                mem[m] = val

# Now sum up all the values
part2 = sum(mem.values())
print(f'Part 2: {part2}')

# Part 1: 14954914379452
# Part 2: 3415488160714
