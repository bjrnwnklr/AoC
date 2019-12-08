from collections import defaultdict

f_name = 'input.txt'

with open(f_name) as f:
    orbits = [l.strip('\n').split(')') for l in f.readlines()]

o_count = defaultdict(int)

for a, b in orbits:
    o_count[b] = o_count[a] + 1

print('Part 1: ', sum(o_count.values()))