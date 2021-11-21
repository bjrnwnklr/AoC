from collections import defaultdict

# f_name = 'ex1.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    numbers = [int(x.strip('\n')) for x in f.readline().split(',')]

turn_mem = defaultdict(int)
# prep the turn memory with the initial list
for turn, num in enumerate(numbers[:-1], start=1):
    turn_mem[num] = turn

last_spoken = numbers[-1]
turns = len(turn_mem) + 1

# cycles = 2020
cycles = 30_000_000

br = 1_000_000

while turns < cycles:
    if last_spoken not in turn_mem:
        next_num = 0
    else:
        next_num = turns - turn_mem[last_spoken]

    turn_mem[last_spoken] = turns
    # print(f'Turn: {turns}. Last spoken: {last_spoken}. Next: {next_num}')

    turns += 1
    last_spoken = next_num

    if turns % br == 0:
        print(f'Turn {turns}. Number {last_spoken}')

print(f'Last spoken after {turns} turns: {last_spoken}')
# Part 1: 412
# Part 2: 243
