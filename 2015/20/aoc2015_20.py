from collections import defaultdict


def calc_presents(n):
    result = n * 10
    for i in range(1, (n // 2) + 1):
        if n % i == 0:
            # print(i)
            result += i * 10

    return result


def calc_all_visits(n):
    houses = defaultdict(int)
    for elf in range(1, n // 10):
        for house in range(elf, n // 10, elf):
            houses[house] += elf * 10

    return houses


def calc_all_visits_pt2(n):
    houses = defaultdict(int)
    for elf in range(1, n // 10):
        for house in range(elf, elf * 51, elf):
            houses[house] += elf * 11

    return houses

if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        req_presents = int(f.readline().strip())

    n = 29_000_000
    houses = calc_all_visits(n)
    h_min = min([h for h in houses if houses[h] >= n])
    print(h_min, houses[h_min])

    # Part 1: 665280

    houses = calc_all_visits_pt2(n)
    h_min = min([h for h in houses if houses[h] >= n])
    print(h_min, houses[h_min])

    # Part 2: 705600
