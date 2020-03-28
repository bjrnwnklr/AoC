from itertools import combinations_with_replacement


# _ + _ * _^2 + _^3 - _ = 399
# coins = [3, 4, 5, 7, 8]

for c in combinations_with_replacement(range(10), 5):
    formula = c[0] + c[1] * c[2]**2 + c[3]**3 - c[4]
    if formula == 399:
        print(c, formula)

