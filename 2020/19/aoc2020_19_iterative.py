import re
import timeit

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
# start with rule 0 and replace any occurrences of digits with their rule representation
rule_zero = rules[0]
# find all digits in rule 0
digits = set(map(int, re.findall(r'(\d+)', rule_zero)))

while digits:
    to_replace = digits.pop()
    rule_to_insert = rules[to_replace]
    # if the rule is atomic (i.e. a or b, or a simple statement without any OR |),
    # don't enclose in parentheses. Only enclose otherwise.
    if rule_to_insert not in ['a', 'b'] and '|' in rule_to_insert:
        rule_to_insert = f'({rule_to_insert})'
    # construct replacement pattern to find only the number (between word boundaries)
    # and then replace all occurrences in the rule_zero
    replacement_pattern = r'\b(' + str(to_replace) + r')\b'
    rule_zero = re.sub(replacement_pattern, rule_to_insert, rule_zero)
    # recreate the digits contained in the updated rule_zero string
    digits = set(map(int, re.findall(r'(\d+)', rule_zero)))

print(timeit.default_timer() - start_time)
# now flatten the pattern by removing all blanks and adding start and end anchors
rule_zero = r'^' + re.sub(r'\s', '', rule_zero) + r'$'
# compile the rule, then match on each message
comp_re = re.compile(rule_zero)

part1 = sum(1 if comp_re.search(m) else 0 for m in messages)
print(f'Part 1: {part1}')

# Part 1: 168
