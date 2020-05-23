import re
from collections import defaultdict

f_name = 'input.txt'
# f_name = 'ex1.txt'

bots = defaultdict(list)
output_bins = defaultdict(list)
instructions = dict()

with open(f_name, 'r') as f:
    for line in f.readlines():
        if 'value' in line:
            val, bot = map(int, re.findall('\d+', line))
            bots[bot].append(val)
        else:
            # process instructions. These need to be in the same order as read
            bot, low_recip, high_recip = map(int, re.findall('\d+', line))
            # find if we are giving to a bot or to output bin
            low_type = 'bot' if re.search('low to bot', line) else 'output'
            high_type = 'bot' if re.search('high to bot', line) else 'output'
            instructions[bot] = (low_type, low_recip, high_type, high_recip)

print(bots)

# find bot with two chips
while True:
    curr_bot = [x for x in bots if len(bots[x]) == 2][0]

    low_type, low_recip, high_type, high_recip = instructions[curr_bot]
    low = min(bots[curr_bot])
    high = max(bots[curr_bot])
    # find our end condition
    if low == 17 and high == 61:
        print(f'Found bot: {curr_bot}')
        break
    # pass on the chips
    if low_type == 'bot':
        bots[low_recip].append(low)
    else: 
        output_bins[low_recip].append(low)
    if high_type == 'bot':
        bots[high_recip].append(high)
    else:
        output_bins[high_recip].append(high)
    # clear the chips the bot holds
    bots[curr_bot] = []

# part 1: 93