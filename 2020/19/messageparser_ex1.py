from ply import lex, yacc
import messagelex

tokens = messagelex.tokens


def p_r0(p):
    """0 : 4 1 5"""
    pass


def p_r1(p):
    """1 : 2 3
         | 3 2"""
    pass


def p_r2(p):
    """2 : 4 4
         | 5 5"""
    pass


def p_r3(p):
    """3 : 4 5
         | 5 4"""
    pass


def p_r4(p):
    """4 : A"""
    pass


def p_r5(p):
    """5 : B"""
    pass


def p_error(p):
    if p:
        raise ValueError("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")
