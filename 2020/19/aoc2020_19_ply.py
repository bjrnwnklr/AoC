import re
from ply import lex, yacc
import messagelex
import messageparser

f_name = 'ex2.txt'
# f_name = 'input.txt'

with open(f_name, 'r') as f:
    raw_rules, raw_messages = f.read().split('\n\n')

# process the messages and store in a list
messages = [x.strip() for x in raw_messages.strip().split('\n')]

# build the lexer
lexer = lex.lex(module=messagelex)
parser = yacc.yacc(module=messageparser, debug=True)
valid_count = 0
for m in messages:
    try:
        result = parser.parse(m)
        valid_count += 1
        print(f'Valid syntax: {m}')
    except ValueError:
        print(f'Incorrect syntax: {m}')


print(f'Valid messages: {valid_count}')
# Part 1: 168
