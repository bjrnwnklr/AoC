import re
from collections import defaultdict
from itertools import permutations


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    guests = defaultdict(defaultdict)
    regex = re.compile(r'^(\w+)\swould\s(\w+)\s(\d+)\shappiness units by sitting next to\s(\w+)\b')
    with open(f_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            m = regex.match(line.strip())
            if m:
                a = m.group(1)
                pm = 1 if m.group(2) == 'gain' else -1
                amount = pm * int(m.group(3))
                b = m.group(4)
                guests[a][b] = amount

    seating_arrangements = [c for c in permutations(guests) if c[0] == 'Alice']
    part1 = max(sum(guests[a][b] + guests[b][a] for a, b in zip(s, s[1:] + s[:1])) for s in seating_arrangements)
    # for s in seating_arrangements:
    #     happiness = 0
    #     for a, b in zip(s, s[1:] + s[:1]):
    #         happiness += guests[a][b] + guests[b][a]
    #     print(f'{happiness}: {s}')
    print(part1)

    # Part 1: 664

    for g in guests:
        guests[g]['you'] = 0
    guests['you'] = defaultdict(int)
    seating_arrangements = [c for c in permutations(guests) if c[0] == 'Alice']
    part2 = max(sum(guests[a][b] + guests[b][a] for a, b in zip(s, s[1:] + s[:1])) for s in seating_arrangements)
    print(part2)

    # Part 2: 640
