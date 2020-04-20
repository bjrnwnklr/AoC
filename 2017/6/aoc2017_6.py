# read in tab separated file
f_name = 'input.txt'

with open(f_name, 'r') as f:
    banks = [int(x) for x in f.readline().strip('\n').split('\t')]

print(banks)

# set of seen configurations
seen = dict()
# number of banks
num_banks = len(banks)
# number of cycles run
cycles = 0

while (tuple(banks) not in seen):
    # add tuple of bank config to seen
    seen[tuple(banks)] = cycles

    # increase cycle count
    cycles += 1

    # print(f'{cycles}: {banks}')

    # select bank with most blocks
    max_blocks = max(banks)
    i_max = banks.index(max_blocks)
    # print(f'{max_blocks} blocks found at {i_max}.')

    # set current blocks to 0
    banks[i_max] = 0

    # step counter for distributing
    i = (i_max + 1) % num_banks

    # redistribute blocks
    while max_blocks:
        banks[i] += 1
        max_blocks -= 1
        i = (i + 1) % num_banks 

print(f'Found same configuration after {cycles} cycles.')
print(f'Part 2: Loop size: {cycles - seen[tuple(banks)]}.')

# Part 1: 12841
# Part 2: 8038

