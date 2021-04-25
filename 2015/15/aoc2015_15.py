import re
from itertools import product


def zip_prod(list_of_tuples):
    result = 0
    for t in list_of_tuples:
        result += t[0] * t[1]
    return result if result > 0 else 0

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

    comb = [x for x in product(range(101), repeat=len(ingredients)) if sum(x) == 100]

    ings_zipped = list(zip(*ingredients.values()))[:4]
    scores = []
    for c in comb:
        score = 1
        for i in ings_zipped:
            props = list(zip(c, i))
            score *= zip_prod(props)
        scores.append(score)

    part1 = max(scores)
    print(f'Part 1: {part1}')

    # Part 1: 21367368
