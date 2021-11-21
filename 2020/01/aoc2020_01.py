f_name = 'input.txt'

with open(f_name, 'r') as f:
    numbers = [int(x.strip('\n')) for x in f.readlines()]

for n in numbers:
    if (d := 2020 - n) in numbers:
        print(f'Part 1: Found {n} + {d} = 2020. Product: {n * d}')

# Part 1: 539851

# Part 2:

for n in numbers:
    d = 2020 - n
    for m in numbers:
        if m != n:
            if (a := d - m) in numbers:
                if a != n and a != m:
                    print(f'Part 2: Found {n} + {m} + {a} = 2020. Product: {n * m * a}')

# Part 2: 212481360