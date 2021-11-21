from functools import reduce

# f_name = 'ex1.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    earliest_depart = int(f.readline())
    busses = [int(n.strip('\n')) for n in f.readline().split(',') if n != 'x']

min_bus_id = 0
min_wait = 1000

for b in busses:
    wait = b - (earliest_depart % b)
    if wait < min_wait:
        min_wait = wait
        min_bus_id = b

print(f'Next bus is #{min_bus_id} departing in {min_wait} minutes. Part 1: {min_bus_id * min_wait}.')


# Part 1: Next bus is #827 departing in 5 minutes. Part 1: 4135.

# Part 2, using chinese remainder theorem


def chinese_remainder(n, a):
    sum_cr = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum_cr += a_i * mul_inv(p, n_i) * p
    return sum_cr % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


# read in the file again, this time not skipping the xs
# ignore the first line
with open(f_name, 'r') as f:
    f.readline()
    all_busses = [x.strip('\n') for x in f.readline().split(',')]

# generate the required bus numbers and remainders
bus_numbers = []
remainders = []
for i, n in enumerate(all_busses):
    if n != 'x':
        bus_numbers.append(int(n))
        remainders.append(int(n) - i)

print(chinese_remainder(bus_numbers, remainders))

# part 2: 640856202464541
