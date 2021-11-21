import re
from collections import defaultdict

header = """from ply import lex, yacc
import messagelex

tokens = messagelex.tokens

"""

error_def = """
def p_error(p):
    if p:
        raise ValueError("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")
"""


def generate_tree(rule, level):
    global treelevels
    global deepestlevel

    deepestlevel[rule] = level
    if rule not in treelevels[level]:
        treelevels[level].append(rule)

    subrules = rules[rule]
    for r in list(map(int, re.findall(r'\d+', subrules))):
        generate_tree(r, level + 1)


def write_rule(rule, f):
    subrules = rules[rule]
    f.write(f'\ndef p_r{rule}(p):\n')
    # handle a and b values
    if subrules in 'ab':
        subrules_text = subrules.upper()
    elif '|' in subrules:
        subrules_text = re.sub(r'\s\|\s', '\n        | ', subrules)
    else:
        subrules_text = subrules

    f.write('    ' + r'"""' + str(rule) + ' : ' + subrules_text + r'"""')
    f.write('\n    pass\n\n')

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

with open('messageparser.py', 'w') as f:
    # write header
    f.write(header)

    for level in sorted(treelevels):
        for r in treelevels[level]:
            if deepestlevel[r] == level:
                write_rule(r, f)

    f.write(error_def)
