import re
from itertools import product


def zip_prod(list_of_tuples):
    result = 0
    for t in list_of_tuples:
        result += t[0] * t[1]
    return result if result > 0 else 0


def solve(ingredients):
    comb = [x for x in product(range(101), repeat=len(ingredients)) if sum(x) == 100]

    all_ings_zipped = list(zip(*ingredients.values()))
    ings_zipped = all_ings_zipped[:4]
    calories = all_ings_zipped[4]

    scores1 = []
    scores2 = []
    for c in comb:
        cals = zip(c, calories)
        total_cals = zip_prod(cals)

        score = 1
        for i in ings_zipped:
            props = list(zip(c, i))
            score *= zip_prod(props)
        scores1.append(score)
        if total_cals == 500:
            scores2.append(score)

    return max(scores1), max(scores2)

if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    regex = re.compile(r'(-*\d+)')

    ingredients = dict()
    with open(f_name, 'r') as f:
        for line in f.readlines():
            ing = line.split(':')[0]
            m = regex.findall(line.strip())
            if m:
                ingredients[ing] = list(map(int, [x for x in m]))

    part1, part2 = solve(ingredients)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')

    # Part 1: 21367368
    # Part 2: 1766400
