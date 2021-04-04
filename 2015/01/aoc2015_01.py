# f_name = 'ex1.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    line = f.readline().strip()

# count the number open and closing parantheses. The resulting delta is the floor.

op = line.count('(')
cp = line.count(')')

part1 = op - cp
print(part1)

# Part 1: 232

floor = 0
char = 0
steps = list(line)

while floor != -1:
    c = steps.pop(0)
    floor += 1 if c == '(' else -1
    char += 1

print(char)