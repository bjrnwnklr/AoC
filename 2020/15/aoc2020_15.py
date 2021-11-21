from collections import defaultdict

# f_name = 'ex1.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    numbers = [int(x.strip('\n')) for x in f.readline().split(',')]

turn_mem = defaultdict(list)
# prep the turn memory with the initial list
for turn, num in enumerate(numbers, start=1):
    turn_mem[num].append(turn)

# we have already done these many turns and the last number said was:
turns = len(numbers)
last_num = numbers[-1]

turns_1 = 2020
turns_2 = 30_000_000

br = 1_000_000

# now the game starts
while turns < turns_2:
    # increase turns count since we started a new turn
    turns += 1
    previous_turns = turn_mem[last_num]
    # if the number was not spoken before, store the turn
    if len(previous_turns) == 1:
        last_num = 0
    else:
        # number was spoken before, get the last two turns
        last_num = previous_turns[-1] - previous_turns[-2]

    turn_mem[last_num].append(turns)
    if turns % br == 0:
        print(f'Turn {turns}. Number {last_num}')

print(f'Turn {turns}. Number {last_num}')

# Part 1: 412
# Part 2: 243
