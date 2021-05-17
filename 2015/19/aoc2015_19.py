import re
from collections import defaultdict, deque
from heapq import heappop, heappush


def heuristic(target, v_next):
    return len(v_next) - len(target)


def sub_iter(pattern, repl, text):
    return [text[:m.start()] + repl + text[m.end():] for m in re.finditer(pattern, text)]


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        top, bottom = f.read().split('\n\n')

    lines = top.strip().split('\n')
    cal_molecule = bottom.strip()

    distinct_molecules = set()
    recipes = defaultdict(list)
    reverse_recipes = dict()

    for line in lines:
        left, right = line.split(' => ')
        recipes[left].append(right)
        reverse_recipes[right[::-1]] = left[::-1]
        for new_text in sub_iter(left, right, cal_molecule):
            distinct_molecules.add(new_text)

    print(len(distinct_molecules))

    # part 1: 576

    # # Part 2 starts here

    # Greedy from the right
    curr_mol = cal_molecule[::-1]
    steps = 0

    while curr_mol != 'e':
        min_start = 10000
        min_end = 10000
        min_pattern = ''
        for pattern in reverse_recipes:
            m = re.search(pattern, curr_mol)
            if m:
                if m.start() < min_start:
                    min_pattern = pattern
                    min_start = m.start()
                    min_end = m.end()

        curr_mol = curr_mol[:min_start] + reverse_recipes[min_pattern] + curr_mol[min_end:]
        steps += 1

    print(steps)

    # Part 2: 207 (for some reason, greedy replacement from the right seems to work...)
