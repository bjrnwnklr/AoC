import re
from collections import defaultdict
#import nltk


def generate_tree(rule, level):
    global treelevels
    global deepestlevel

    deepestlevel[rule] = level
    if rule not in treelevels[level]:
        treelevels[level].append(rule)

    subrules = rules[rule]
    for r in list(map(int, re.findall(r'\d+', subrules))):
        generate_tree(r, level + 1)


def write_rule(rule):
    subrules = rules[rule]
    temp_text = f'{rule} -> '
    # handle a and b values
    if subrules in 'ab':
        subrules_text = f'\"{subrules}\"'
    else:
        subrules_text = subrules

    temp_text += subrules_text + '\n'
    return temp_text

f_name = 'ex2.txt'
# f_name = 'input.txt'

with open(f_name, 'r') as f:
    raw_rules, _ = f.read().split('\n\n')

rules = dict()
for rule in raw_rules.split('\n'):
    rule_num, subrules = rule.split(':')
    rules[int(rule_num)] = subrules.strip().strip('\"')

# generate the tree
treelevels = defaultdict(list)
deepestlevel = defaultdict(int)
generate_tree(0, 0)

cfg = ''
for level in sorted(treelevels):
    for r in treelevels[level]:
        if deepestlevel[r] == level:
            cfg += write_rule(r)

print(cfg)