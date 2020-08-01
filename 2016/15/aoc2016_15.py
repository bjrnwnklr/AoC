import re

# f_name = 'input.txt'
f_name = 'input2.txt'

with open(f_name, 'r') as f:
    discs = [tuple(map(int, re.findall(r'(\d+)', line))) for line in f.readlines()]

# simulate the discs
found = False
t = 0
num_discs = len(discs)

while not found:
    found = all(((t + d + discs[d-1][3]) % discs[d-1][1] == 0) for d in range(1, num_discs + 1))
    t += 1

print(t - 1)
        
# part 1: 148737
# part 2: 2353212

