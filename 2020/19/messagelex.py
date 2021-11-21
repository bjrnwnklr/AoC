from ply import lex, yacc

# first definitions of the tokens for lex:
tokens = (
    'A',
    'B'
)

# Regular expression rules for simple tokens
t_A = r'a'
t_B = r'b'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# to ignore spaces or tabs
t_ignore = ' \t'


# error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lex.lex()
