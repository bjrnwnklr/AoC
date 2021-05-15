from itertools import combinations
from collections import defaultdict


if __name__ == '__main__':

    # eggnog = 25
    eggnog = 150

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    containers = []
    with open(f_name, 'r') as f:
        for line in f.readlines():
            containers.append(int(line.strip()))

    print(containers)

    valid_combos = 0
    d = defaultdict(int)
    for n in range(1, len(containers) + 1):
        val = list(filter(lambda x: sum(x) == eggnog, combinations(containers, n)))
        valid_combos += len(val)
        for v in val:
            d[len(v)] += 1

    print(valid_combos)
    m = min(d)
    print(d[m])

    # Part 1: 4372
    # Part 2: 4

