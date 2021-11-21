from ply import lex, yacc
import messagelex

tokens = messagelex.tokens


def p_r0(p):
    """0 : 8 11"""
    pass


def p_r8(p):
    """8 : 42"""
    pass


def p_r11(p):
    """11 : 42 31"""
    pass


def p_r42(p):
    """42 : 9 14
        | 10 1"""
    pass


def p_r31(p):
    """31 : 14 17
        | 1 13"""
    pass


def p_r9(p):
    """9 : 14 27
        | 1 26"""
    pass


def p_r10(p):
    """10 : 23 14
        | 28 1"""
    pass


def p_r17(p):
    """17 : 14 2
        | 1 7"""
    pass


def p_r13(p):
    """13 : 14 3
        | 1 12"""
    pass


def p_r27(p):
    """27 : 1 6
        | 14 18"""
    pass


def p_r26(p):
    """26 : 14 22
        | 1 20"""
    pass


def p_r23(p):
    """23 : 25 1
        | 22 14"""
    pass


def p_r28(p):
    """28 : 16 1"""
    pass


def p_r2(p):
    """2 : 1 24
        | 14 4"""
    pass


def p_r7(p):
    """7 : 14 5
        | 1 21"""
    pass


def p_r3(p):
    """3 : 5 14
        | 16 1"""
    pass


def p_r12(p):
    """12 : 24 14
        | 19 1"""
    pass


def p_r1(p):
    """1 : A"""
    pass


def p_r6(p):
    """6 : 14 14
        | 1 14"""
    pass


def p_r18(p):
    """18 : 15 15"""
    pass


def p_r22(p):
    """22 : 14 14"""
    pass


def p_r20(p):
    """20 : 14 14
        | 1 15"""
    pass


def p_r25(p):
    """25 : 1 1
        | 1 14"""
    pass


def p_r16(p):
    """16 : 15 1
        | 14 14"""
    pass


def p_r24(p):
    """24 : 14 1"""
    pass


def p_r4(p):
    """4 : 1 1"""
    pass


def p_r5(p):
    """5 : 1 14
        | 15 1"""
    pass


def p_r21(p):
    """21 : 14 1
        | 1 14"""
    pass


def p_r19(p):
    """19 : 14 1
        | 14 14"""
    pass


def p_r14(p):
    """14 : B"""
    pass


def p_r15(p):
    """15 : 1
        | 14"""
    pass


def p_error(p):
    if p:
        raise ValueError("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")
