f_name = 'ex1.txt'
# f_name = 'input.txt'

with open(f_name, 'r') as f:
    line = f.readlines()[1]
    schedule = [(int(n), (int(n) - i) % int(n)) for i, n in enumerate(line.strip().split(',')) if n != 'x']

print(schedule)

a = 0
b = 1

for c, z in schedule:
    found = False
    n = 0
    while not found:
        if (a + b * n) % c == z:
            print(f'Found for bus {c}: departure at {a + b * n}')
            a = a + b * n
            b *= c
            found = True
        n += 1

print(a)

