from functools import lru_cache
import sys

@lru_cache(50000)
def f_6027(m, n):
    if m == 0:
        return n + 1
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
            memoization[(m, n)] = n + 1
            return n + 1
        elif n == 0:
            r = f_6027(m-1, k)
            memoization[(m, n)] = r
            return r
        else:
            r = f_6027(m-1, f_6027(m, n-1))
            memoization[(m, n)] = r
            return r


memoization = dict()
sys.setrecursionlimit(1000000)
print('starting')
k = 25468
r = f_6027_memo(4, 0)
print('ended')
print(r)