import re
from ply import lex, yacc

# Using the example code from PLY docs to define our simple grammar / tokens

# --------- LEX definition ---------

# first definitions of the tokens for lex:
tokens = (
    'NUMBER',
    'PLUS',
    'TIMES',
    'LPAREN',
    'RPAREN'
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'


# NUMBER
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# to ignore spaces or tabs
t_ignore = ' \t'


# error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# ------------ YACC configuration ------------
"""
Our grammar is the following:
expression : expression PLUS expression
             | expression TIMES expression
             | LPAREN expression RPAREN
             | NUMBER
           
This requires the definition of precedence as otherwise it is not clear in which order
PLUS and TIMES should be processed.
"""


def p_expression(p):
    """expression : expression PLUS expression
                  | expression TIMES expression
    """
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]


def p_expression_expr(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_num(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        expressions = [l.strip('\n') for l in f.readlines()]

    # build the lexer
    lexer = lex.lex()

    # # feed the input and give the lexer input - only required if we want to test the output
    # for e in expressions:
    #     lexer.input(e)
    #     for tok in lexer:
    #         print(tok)

    # define precedence for part 1 - PLUS and TIMES have same precedence
    # Note it is important to add the comma to the end, as precedence expects a tuple of tuples
    precedence = (
        ('left', 'PLUS', 'TIMES'),
    )

    parser = yacc.yacc()
    # for e in expressions:
    #     result = parser.parse(e)
    #     print(result)

    part1 = sum(parser.parse(e) for e in expressions)
    print(f'Part 1: {part1}')

    # define precedence for part 2 - TIMES has lower precedence than PLUS
    precedence = (
        ('left', 'TIMES'),
        ('left', 'PLUS')
    )
    parser = yacc.yacc()
    # for e in expressions:
    #     result = parser.parse(e)
    #     print(result)

    part2 = sum(parser.parse(e) for e in expressions)
    print(f'Part 2: {part2}')

    # Part 1: 86311597203806
    # Part 2: 276894767062189
