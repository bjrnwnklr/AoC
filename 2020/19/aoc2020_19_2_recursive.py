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


# f_name = 'ex2.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    raw_rules, raw_messages = f.read().split('\n\n')

# process the messages and store in a list
messages = [x.strip() for x in raw_messages.strip().split('\n')]

# process the rules and save them in a dict
rules = dict()
for rule in raw_rules.split('\n'):
    rule_num, subrules = rule.split(':')
    rule_num = int(rule_num)
    # process subrules and store in rules directory
    # for example 2, the longest message is 45 characters.
    # since rule 8 is a match of 5 characters, we could extend to a maximum of 9 repetitions
    # since rule 11 is a match of 10 characters (5 for rule 42, 5 for rule 31), we could extend by 5 repetitions

    # for the input, the longest message is 96 characters
    # so we need to replace rule 8 with up to 20 repetitions
    # and rule 11 with up to 10 repetitions
    if rule_num == 8:
        rules[rule_num] = ' | '.join(' '.join(['42'] * i) for i in range(1, 21))
    elif rule_num == 11:
        rules[rule_num] = ' | '.join(' '.join(['42'] * i + ['31'] * i) for i in range(1, 11))
    else:
        rules[rule_num] = subrules.strip().strip('\"')

start_time = timeit.default_timer()
# start with rule 0 and replace any occurrences of digits with their rule representation
rule_zero = expand_rule(0)
print(timeit.default_timer() - start_time)

# now flatten the pattern by removing all blanks and adding start and end anchors
rule_zero = r'^' + rule_zero + r'$'
# compile the rule, then match on each message
comp_re = re.compile(rule_zero)

part1 = sum(1 if comp_re.search(m) else 0 for m in messages)
print(f'Part 1: {part1}')

# Part 1: 168
# Part 2: 277
