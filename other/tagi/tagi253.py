"""
Tagi Zahlendreher 253: https://www.tagesanzeiger.ch/die-minimale-summe-674003274085
"""
from itertools import permutations


def summe_zeilen_gleich(p):
    """Return True if sum of the top and bottom row (0-2, 5-7) are equal"""
    return sum([p[i] for i in range(3)]) == sum([p[i] for i in range(5, 8)])


def summe_spalten_gleich(p):
    """Return True if sum of the left and right columns (0, 3, 5, and 2, 4, 7) are equal"""
    return sum([p[0], p[3], p[5]]) == sum([p[2], p[4], p[7]])


def summe_ecken(p):
    """Return the sum of the 4 corners (0, 2, 5, 7)"""
    return p[0] + p[2] + p[5] + p[7]


def minimale_summe():
    """
    Schreibe die Zahlen von 1 bis 8 in die Zellen der Tabelle und zwar so, 
    dass die Summen der Zahlen in den beiden Zeilen (oben und unten) 
    und in der beiden Spalten (rechts und links) gleich sind.

    Welches ist die minimale Summe der Zahlen in den 4 Ecken der Tabelle?
    """
    min_summe = 100
    min_p = ''
    for p in permutations(range(1, 9)):
        if summe_spalten_gleich(p) and summe_zeilen_gleich(p):
            r = summe_ecken(p)
            if r < min_summe:
                min_summe = r
                min_p = p

    print(f'{list[min_p]}')

    return min_summe


if __name__ == '__main__':

    r1 = minimale_summe()
    print(f'Minimale Summe: {r1}')
