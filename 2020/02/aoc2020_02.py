f_name = 'input.txt'

valid_pws = 0

with open(f_name, 'r') as f:
    for line in f.readlines():
        r, c, pw = line.strip('\n').split(' ')
        l, h, = map(int, r.split('-'))
        c = c[0]
        policy_count = pw.count(c)
        if l <= policy_count <= h:
            valid_pws += 1


print(f'Part 1: counted {valid_pws} valid passwords.')

# Part 1: 548

# Part 2

valid_pws = 0

with open(f_name, 'r') as f:
    for line in f.readlines():
        r, c, pw = line.strip('\n').split(' ')
        l, h, = map(int, r.split('-'))
        c = c[0]

        if sum(pw[pos - 1] == c for pos in [l, h]) == 1:
            valid_pws += 1

print(f'Part 2: counted {valid_pws} valid passwords.')

# Part 2: 502
