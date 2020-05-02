

f_name = 'input.txt'

with open(f_name, 'r') as f:
    start_vals = [int(line.strip('\n')[-3:]) for line in f.readlines()]

# start_vals = [65, 8921]

factors = [16807, 48271]
mults = [4, 8]
modval = 2147483647

def gen_val(prev, factor, m):
    val = (prev * factor) % modval
    if (val % m) == 0:
        return val
    else:
        return(gen_val(val, factor, m))

next_val = start_vals[:]
cycles = 5_000_000
matches = 0
for c in range(cycles):
    next_val = [gen_val(next_val[i], factors[i], mults[i]) for i in range(2)]
    bin_val = [f'{x:016b}'[-16:] for x in next_val]
    if bin_val[0] == bin_val[1]:
        matches += 1

    if (c % 100_000 == 0):
        print(f'{c}:\t{matches}')

print(matches)

# Part 1: 619
# Part 2: 290