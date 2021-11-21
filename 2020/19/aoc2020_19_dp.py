import re
import timeit
from collections import defaultdict

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
    rule_num = int(rule_num)
    subrules = subrules.strip()
    # clean up "a" and "b" by removing the quotes
    if 'a' in subrules or 'b' in subrules:
        subrules = re.sub('\"', '', subrules)
    # process subrules and store in rules directory
    rules[rule_num] = subrules

start_time = timeit.default_timer()

# create a copy of the rules to check if there is a | in any rule
orig_rules = rules.copy()

# set up some structures to handle the storing of completed rules
finalized_queue = []

# create a dict of which rule is contained in which, and create the initial queue of finalized rules from the
# atomic cases ('a' and 'b')
contained_in = defaultdict(set)
for rule in rules:
    rule_to_check = rules[rule]
    if rule_to_check in ['a', 'b']:
        finalized_queue.append(rule)
        continue

    for r in list(re.findall(r'\d+', rules[rule])):
        contained_in[int(r)].add(rule)

reverse_list = []
while finalized_queue:
    rule = finalized_queue.pop(0)
    reverse_list.append(rule)
    prefix = suffix = ''
    if '|' in orig_rules[rule]:
        prefix = '('
        suffix = ')'
    updated_rule = prefix + rules[rule] + suffix
    for rule_to_update in contained_in[rule]:
        string_to_change = re.sub(r'\b' + str(rule) + r'\b', updated_rule, rules[rule_to_update])
        # check if there are any digits left to replace, if not finalize the rule
        if not re.search(r'\d+', string_to_change):
            # strip out any blanks
            string_to_change = re.sub(r'\s', '', string_to_change)
            # this rule is now finalized, so store it and add it to the queue to process next
            finalized_queue.append(rule_to_update)
        rules[rule_to_update] = string_to_change

rule_zero = rules[0]

print(timeit.default_timer() - start_time)
# now flatten the pattern by removing all blanks and adding start and end anchors
rule_zero = r'^' + re.sub(r'\s', '', rule_zero) + r'$'
# compile the rule, then match on each message
comp_re = re.compile(rule_zero)

part1 = sum(1 if comp_re.search(m) else 0 for m in messages)
print(f'Part 1: {part1}')

print(reverse_list[::-1])

# Part 1: 168
