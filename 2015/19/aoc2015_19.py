import re
from collections import defaultdict


def sub_iter(pattern, repl, text):
    return [text[:m.start()] + repl + text[m.end():] for m in re.finditer(pattern, text)]


if __name__ == '__main__':

    f_name = 'ex1.txt'
    # f_name = 'input.txt'

    with open(f_name, 'r') as f:
        top, bottom = f.read().split('\n\n')

    lines = top.strip().split('\n')
    cal_molecule = bottom.strip()

    distinct_molecules = set()
    recipes = defaultdict(list)

    for line in lines:
        left, right = line.split(' => ')
        recipes[left].append(right)
        for new_text in sub_iter(left, right, cal_molecule):
            distinct_molecules.add(new_text)

    print(len(distinct_molecules))

    # part 1: 576

    # Part 2 starts here
    start = 'e'
    end = cal_molecule


