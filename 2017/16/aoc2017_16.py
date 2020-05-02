

# f_name = 'ex1.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    moves = [x for x in f.readline().strip('\n').split(',')]

n = 16
programs = [chr(i) for i in range(97, 97 + n)]

start = ''.join(programs)

cycles = 1_000_000_000

# Every 44 cycles, the programs are in their start position, so we only need to run 
# 1_000_000_000 % 44 times

req_cycles = cycles % 44
print(f'Required cycles are: {req_cycles}')

for c in range(req_cycles):

    for m in moves:
        if m[0] == 's':
            x = int(m[1:])
            programs = programs[-x:] + programs[:-x]
        elif m[0] == 'x':
            a, b = map(int, m[1:].split('/'))
            programs[a], programs[b] = programs[b], programs[a]
        elif m[0] == 'p':
            a, b = m[1:].split('/')
            ind_a, ind_b = programs.index(a), programs.index(b)
            programs[ind_a], programs[ind_b] = programs[ind_b], programs[ind_a]

    if ''.join(programs) == start:
        print(f'Matching start after cycle {c}.')

    if (c % 1_000) == 0:
        print(f'Cycle {c}')

print(''.join(programs))

# part 1: kpbodeajhlicngmf

# part 2: ahgpjdkcbfmneloi (after 32 moves - 1_000_000_000 % 44)


