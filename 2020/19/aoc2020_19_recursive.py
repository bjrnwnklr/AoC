import re
from functools import lru_cache
import timeit


@lru_cache
def expand_rule(r):
    rule = rules[r]
    # atomic case - if we have an 'a' or 'b'
    if rule in 'ab':
        return rule
    prefix = suffix = ''
    # handle a | in the rule - enclose with parentheses
    if '|' in rule:
        prefix = '('
        suffix = ')'
    # expand all included rules
    return prefix + ''.join(expand_rule(int(x)) if x != '|' else x for x in rule.split()) + suffix


# f_name = 'ex1.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    raw_rules, raw_messages = f.read().split('\n\n')

# process the messages and store in a list
messages = [x.strip() for x in raw_messages.strip().split('\n')]

# process the rules and save them in a dict
rules = dict()
for rule in raw_rules.split('\n'):
    rule_num, subrules = rule.split(':')
    rules[int(rule_num)] = subrules.strip().strip('\"')

start_time = timeit.default_timer()
# start with rule 0 and replace any occurrences of digits with their rule representation
rule_zero = expand_rule(0)
print(timeit.default_timer() - start_time)

# now flatten the pattern by removing all blanks and adding start and end anchors
rule_zero = r'^' + rule_zero + r'$'
# compile the rule, then match on each message
comp_re = re.compile(rule_zero)

for m in messages:
    if comp_re.match(m):
        print(f'Valid syntax: {m}')
    else:
        print(f'Incorrect syntax: {m}')

part1 = sum(bool(comp_re.match(m)) for m in messages)
print(f'Part 1: {part1}')

# Part 1: 168
