import re


sue = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""


def match_comp_1(comp, count):
    return count == sue_vals[comp]


def match_comp_2(comp, count):
    if comp in ('cats', 'trees'):
        result = count > sue_vals[comp]
    elif comp in ('pomeranians', 'goldfish'):
        result = count < sue_vals[comp]
    else:
        result = count == sue_vals[comp]
    return result


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    regex_sue = re.compile(r'Sue (\d+):')
    regex_compounds = re.compile(r'(\w+): (\d+)')

    aunts = dict()
    with open(f_name, 'r') as f:
        for line in f.readlines():
            aunt_num = int(regex_sue.search(line).group(1))
            m = regex_compounds.findall(line.strip())
            if m:
                aunts[aunt_num] = {k: int(v) for k, v in m}

    # get values for the one Aunt Sue
    lines = sue.split('\n')
    m = regex_compounds.findall(sue)
    if m:
        sue_vals = {k: int(v) for k, v in m}
    print(sue_vals)

    matching_sues_1 = set()
    matching_sues_2 = set()
    for k, v in aunts.items():
        if all(match_comp_1(c, n) for c, n in v.items()):
            matching_sues_1.add(k)
        if all(match_comp_2(c, n) for c, n in v.items()):
            matching_sues_2.add(k)

    print(matching_sues_1, matching_sues_2)

    # Part 1: 373
    # Part 2: 260