from functools import lru_cache
import sys

@lru_cache(50000)
def f_6027(m, n):
    if m == 0:
        return (n + 1)
    elif n == 0:
        return f_6027(m-1, k)
    else:
        return f_6027(m-1, f_6027(m, n-1))

def f_6027_memo(m, n):
    global memoization
    if (m, n) in memoization:
        return memoization[(m, n)]
    else:
        if m == 0:
            r = (n + 1) % 32768
        elif n == 0:
            r = f_6027(m-1, k) % 32768
        else:
            r = f_6027(m-1, f_6027(m, n-1)) % 32768

        memoization[(m, n)] = r
        return r

@lru_cache(50000)
def f_6027_opt(m, n):
    if m == 0:
        return (n + 1)
    elif m == 1:
        return n + k + 1
    elif m == 2:
        return n * (k + 1) + 2 * k + 1
    elif m == 3:
        return f_6027_opt(3, m-1) * (k + 1) + 2 * k + 1
    else:
        return f_6027_opt(m-1, f_6027_opt(m, n-1))


memoization = dict()
sys.setrecursionlimit(1000000)
print('starting')
k = 25468
r_non_opt = f_6027_memo(3, 1)
# r_opt = f_6027_opt(2, 1)
print('ended')
# print(r_non_opt, r_opt)
print(r_non_opt)