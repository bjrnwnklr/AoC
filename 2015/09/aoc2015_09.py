import re
from itertools import permutations


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    edges = dict()
    cities = set()
    for line in lines:
        match = re.match(r'(\w+) to (\w+) = (\d+)', line.strip())
        if match:
            f = match.group(1)
            t = match.group(2)
            d = int(match.group(3))
            edges[(f, t)] = d
            edges[(t, f)] = d
            cities.add(f)
            cities.add(t)

    paths = dict()
    for p in permutations(cities):
        distance = 0
        for i in range(len(p) - 1):
            distance += edges[(p[i], p[i + 1])]
        paths[p] = distance

    part1 = min(paths, key=lambda x: paths[x])
    print(part1, paths[part1])

    # part 1: ('Tambi', 'Arbre', 'Snowdin', 'AlphaCentauri', 'Tristram', 'Straylight', 'Faerun', 'Norrath') 251

    part2 = max(paths, key=lambda x: paths[x])
    print(part2, paths[part2])

    # part 2: ('Tristram', 'Faerun', 'Arbre', 'Straylight', 'AlphaCentauri', 'Norrath', 'Tambi', 'Snowdin') 898
