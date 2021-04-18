import re


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
        speed = reindeers[rd][0]
        duration = reindeers[rd][1]
        rest = reindeers[rd][2]
        a = n // (duration + rest)
        remainder = n - a * (duration + rest)
        remaining_km_flown = min(duration, remainder)
        km_flown = speed * (a * duration + remaining_km_flown)
        travelled.append(km_flown)
        print(rd, a, a * (duration + rest), remainder, km_flown)

    print(f'Part 1: {max(travelled)}')

    # Part 1: 2696
