import re
from collections import defaultdict


def travel_km(rd, t):
    speed = reindeers[rd][0]
    duration = reindeers[rd][1]
    rest = reindeers[rd][2]
    a = t // (duration + rest)
    remainder = t - a * (duration + rest)
    remaining_km_flown = min(duration, remainder)
    km_flown = speed * (a * duration + remaining_km_flown)
    return km_flown


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    regex = re.compile(r'(\w+).+\s(\d+).+\s(\d+).+\s(\d+)')
    reindeers = dict()
    with open(f_name, 'r') as f:
        for line in f.readlines():
            m = regex.match(line.strip())
            if m:
                name = m.group(1)
                speed = int(m.group(2))
                duration = int(m.group(3))
                rest = int(m.group(4))
                reindeers[name] = (speed, duration, rest)

    # n = 1000
    n = 2503

    travelled = []
    for rd in reindeers:
        km_flown = travel_km(rd, n)
        travelled.append(km_flown)

    print(f'Part 1: {max(travelled)}')

    # Part 1: 2696

    leading = defaultdict(int)
    for t in range(1, n+1):
        round_traveled = defaultdict(list)
        for rd in reindeers:
            round_traveled[travel_km(rd, t)].append(rd)

        # figure out what happens if multiple reindeer in the lead - they each get one point!
        max_km = max(round_traveled)
        for rd in round_traveled[max_km]:
            leading[rd] += 1
        # print(t, leading)

    print(leading)
    leading_rd = max(leading, key=lambda x: leading[x])
    part2 = leading[leading_rd]
    print(part2)

    # part 2: 1084 (Rudolph)