import re
from collections import Counter, defaultdict

def dist(a, b):
    r = a[3]
    d = sum(abs(a[i] - b[i]) for i in range(3))
    return d <= r

def bot_range(b):
    r = b[3]
    br = {(b[0] + x, b[1] + y, b[2] + z) for x in range(-r, r + 1)
                                         for y in range(-(r - x), r - x + 1)
                                         for z in range(-(r - y), r - y + 1)
                                         if x + y + z <= r}
    return br

bots = []
for l in open('example.txt'):
    x, y, z, r = re.findall(r'-?\d+', l)
    bots.append(tuple(map(int, [x, y, z, r])))

big_bot = max([b for b in bots], key = lambda b: b[3])
print('big bot:', big_bot)

in_range = [b for b in bots if dist(big_bot, b)]

print(len(in_range))

#### part 2

# no part 2 solution for me - it requires a lot of optimized code
