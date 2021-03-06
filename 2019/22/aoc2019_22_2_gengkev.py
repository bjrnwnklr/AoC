#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
# import aocd

flatten = itertools.chain.from_iterable


# is_sample = False
# DAY = 22
# YEAR = 2019


##########################################################################

def deck_deal_new(deck):
    return list(reversed(deck))

def deck_cut(deck, n):
    return deck[n:] + deck[:n]

def deck_deal_inc(deck, n):
    out = [-1 for _ in range(len(deck))]
    for i in range(len(deck)):
        pos = (i * n) % len(deck)
        out[pos] = deck[i]
    assert not any(x == -1 for x in out)
    return out


def mat_identity(N):
    return [[1 if i == j else 0 for j in range(N)] for i in range(N)]

def mat_mult(A, B, mod=0):
    N = len(A)
    M = len(B[0])

    L = len(A[0])
    assert L == len(B)

    C = [[0 for _ in range(M)] for _ in range(N)]
    for i in range(N):
        for j in range(M):
            acc = 0
            for k in range(L):
                acc += A[i][k] * B[k][j]
            if mod != 0:
                acc %= mod
            C[i][j] = acc

    return C

# https://www.hackerearth.com/practice/notes/matrix-exponentiation-1/
def mat_pow(A, exp, mod=0):
    res = mat_identity(2)
    while exp > 0:
        if exp % 2 == 1:
            res = mat_mult(res, A, mod)
        A = mat_mult(A, A, mod)
        exp //= 2
    return res


def main(A):
    NCARDS = 10007
    cards = list(range(NCARDS))  # index 0 is top

    # Solve part 1
    def part1():
        deck = cards[:]
        for line in A:
            tokens, integers = line
            if tokens[0] == 'cut':
                deck = deck_cut(deck, integers[0])
            elif tokens[0:3] == ['deal', 'with', 'increment']:
                deck = deck_deal_inc(deck, integers[0])
            elif tokens[0:4] == ['deal', 'into', 'new', 'stack']:
                deck = deck_deal_new(deck)
            else:
                assert False
            #print('processed', tokens, integers)
            #print('deck', deck)
        #print('result', deck)
        return deck.index(2019)

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        MOD = 119315717514047
        REP = 101741582076661

        ###################################################
        # Compute ax+b for fwd transform
        a = 1
        b = 0

        for line in A:
            tokens, integers = line
            if tokens[0] == 'cut':
                k = integers[0]
                b -= k
            elif tokens[0:3] == ['deal', 'with', 'increment']:
                k = integers[0]
                a *= k
                b *= k
            elif tokens[0:4] == ['deal', 'into', 'new', 'stack']:
                a *= -1
                b = -b - 1
            else:
                assert False

        #print('a = {}, b = {}'.format(a, b))
        a = a % MOD
        b = b % MOD
        #print('a = {}, b = {}'.format(a, b))

        ###################################################
        # Compute inverse
        inv_a = pow(a, MOD-2, MOD)
        inv_b = ((-b) * inv_a) % MOD

        #print('inv_a = {}, inv_b = {}'.format(inv_a, inv_b))

        ###################################################
        # Repeat REP number of times
        # Use matrix exponentiation to do this...
        M = [[inv_a, inv_b], [0, 1]]
        #print('M', M)

        Mexp = mat_pow(M, REP, MOD)
        #print('Mexp', Mexp)

        ###################################################
        # Apply matrix to input value 2020
        v = [[2020], [1]]
        #print('v', v)
        y = mat_mult(Mexp, v, MOD)
        #print('y', y)

        return y[0][0]



    res = part2()
    submit_2(res)


##########################################################################

def parse_line(line):
    integers = re.findall(r'[-+]?\d+', line)
    integers = list(map(int, integers))
    tokens = line.split()
    return (tokens, integers)


def parse_input(A):
    A = A.strip()
    A = A.splitlines()
    A = [parse_line(line) for line in A]
    return A


##########################################################################


def submit_1(res):
    print('Part 1', res)


def submit_2(res):
    print('Part 2', res)


##########################################################################


if __name__ == '__main__':
    # set logging level
    # logging.basicConfig(level=logging.INFO)

    # part 1
    # size = 10007

    # part 2
    f_name = 'input.txt'


    with open(f_name) as f:
        # A = f.strip()
        # A = f.splitlines()
        A = [parse_line(line) for line in f.readlines()]

    main(A)