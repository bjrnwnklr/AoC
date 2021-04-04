from collections import defaultdict

# f_name = 'ex1.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    line = f.readline().strip()

dirs = {
    '<': (0, -1),
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0)
}

houses = defaultdict(int)
pos = (0, 0)
houses[pos] += 1

for d in list(line):
    pos = (pos[0] + dirs[d][0], pos[1] + dirs[d][1])
    houses[pos] += 1

part1 = len(houses)
print(part1)

# Part 1: 2565

houses = defaultdict(int)
positions = [(0, 0), (0, 0)]
houses[(0, 0)] += 2

for d in list(line):
    pos = positions.pop(0)
    pos = (pos[0] + dirs[d][0], pos[1] + dirs[d][1])
    positions.append(pos)
    houses[pos] += 1

part2 = len(houses)
print(part2)

# Part 2: 2639
