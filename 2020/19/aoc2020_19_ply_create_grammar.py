import re

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


rules_order = [0, 11, 8, 42, 31, 112, 39, 14, 73, 74, 139, 138, 116, 62, 113, 35, 32, 85, 13, 17, 90, 122, 29, 7, 9, 86, 77, 19, 95, 24, 54, 105, 66, 55, 34, 60, 56, 43, 83, 37, 68, 119, 129, 96, 97, 111, 27, 58, 125, 53, 80, 124, 81, 23, 41, 22, 118, 2, 6, 93, 84, 127, 28, 50, 10, 25, 117, 82, 79, 135, 36, 67, 30, 91, 115, 49, 46, 78, 71, 4, 5, 99, 33, 64, 21, 110, 45, 107, 69, 3, 120, 52, 12, 106, 134, 61, 114, 137, 103, 133, 1, 130, 57, 59, 51, 123, 104, 136, 101, 65, 126, 15, 108, 75, 128, 132, 47, 38, 131, 63, 26, 121, 40, 70, 48, 76, 20, 109, 102, 100, 94, 92, 88, 87, 72, 44, 18, 98, 89, 16]



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

# f_name = 'ex1.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    raw_rules, _ = f.read().split('\n\n')

rules = dict()
for rule in raw_rules.split('\n'):
    rule_num, subrules = rule.split(':')
    rules[int(rule_num)] = subrules.strip().strip('\"')

with open('messageparser.py', 'w') as f:
    # write header
    f.write(header)

    # write rules
    for rule in rules_order:
        write_rule(rule, f)

    f.write(error_def)
