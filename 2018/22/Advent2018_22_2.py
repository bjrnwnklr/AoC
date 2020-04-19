from functools import lru_cache
from heapq import heappush, heappop

MOD = 20183
depth = 10689
tx, ty = 11, 722

@lru_cache(None)
def gindex(x, y):
    if x == y == 0: return 0
    if x == tx and y == ty: return 0
    if y == 0: return x * 16807 % MOD
    if x == 0: return y * 48271 % MOD
    return ((gindex(x-1, y) + depth) *
            (gindex(x, y-1) + depth) % MOD)

def region(x, y):
    return (gindex(x, y) + depth) % MOD % 3

ans1 = sum(region(x, y)
           for x in range(tx+1)
           for y in range(ty+1))