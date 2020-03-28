from itertools import permutations


# _ + _ * _^2 + _^3 - _ = 399
coins = [2, 3, 5, 7, 9]

for c in permutations(coins, 5):
    formula = c[0] + c[1] * c[2]**2 + c[3]**3 - c[4]
    if formula == 399:
        print(c, formula)

