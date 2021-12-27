from itertools import combinations, product

nums = [-1246,
        -1104,
        -1125,
        168,
        72,
        68,
        -43,
        88,
        113]

for a, b, c in combinations(nums, 3):
    for p, q, r in product([-1, 1], repeat=3):
        x = p * a + q * b + r * c
        if x in [1105, -1205, 1229]:
            print(f'{x=}, {p=} * {a=} + {q=} * {b=} + {r=} * {c=}')
