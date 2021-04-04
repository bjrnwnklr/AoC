import re
from collections import defaultdict


def toggle(r, c):
    grid[(r, c)] = (grid[(r, c)] + 1) % 2


def on(r, c):
    grid[(r, c)] = 1


def off(r, c):
    grid[(r, c)] = 0


def toggle2(r, c):
    grid[(r, c)] += 2


def on2(r, c):
    grid[(r, c)] += 1


def off2(r, c):
    grid[(r, c)] -= 1
    if grid[(r, c)] < 0:
        grid[(r, c)] = 0


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        lines = f.readlines()

    grid = defaultdict(int)

    for line in lines:
        r1, c1, r2, c2 = map(int, re.findall(r'(\d+)', line.strip()))
        if 'toggle' in line:
            f = toggle
        elif 'turn on' in line:
            f = on
        elif 'turn off' in line:
            f = off

        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                f(r, c)

    part1 = sum(light for light in grid.values())
    print(part1)

    # Part 1: 377891

    grid = defaultdict(int)

    for line in lines:
        r1, c1, r2, c2 = map(int, re.findall(r'(\d+)', line.strip()))
        if 'toggle' in line:
            f = toggle2
        elif 'turn on' in line:
            f = on2
        elif 'turn off' in line:
            f = off2

        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                f(r, c)

    part2 = sum(light for light in grid.values())
    print(part2)

    # Part 2: 14110788