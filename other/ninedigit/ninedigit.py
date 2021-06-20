from itertools import permutations


def div_by_digit(n, digit):
    numb = int(n[:digit])
    return numb % digit == 0


for i in permutations(range(1, 10), 9):
    if all(div_by_digit(''.join(str(c) for c in i), digit) for digit in range(1, 10)):
        print(i)
