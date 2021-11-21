# f_name = 'ex1.txt'
f_name = 'input.txt'

all_ingredients = set()
possible_allergens = dict()
recipes = list()

with open(f_name, 'r') as f:
    for i, line in enumerate(f.readlines()):
        # get a list of the ingredients and record the food recipe as a set of the
        # ingredients (recipes = [{'aaa', 'bbb'}, {...}]
        ingredients = line.split(' (')[0].strip().split()
        recipes.append(set(ingredients))
        
        all_ingredients |= set(ingredients)
        # get a list of the allergens and store a dict of allergens with the food it is
        # contained in (allergens_in_food[dairy] = {1, 2, 3...}
        allergens = line.split(' (')[1][9:-2].strip().split(', ')

        for a in allergens:
            if a not in possible_allergens:
                possible_allergens[a] = set(ingredients)
            else:
                possible_allergens[a] &= set(ingredients)

# Part 1: count occurence of each ingredient not a possible allergen in the recipes
all_possible_allergens = set((x for ing_set in possible_allergens.values() for x in ing_set))
no_allergens = all_ingredients - all_possible_allergens

part1 = 0
for ing in no_allergens:
    part1 += sum(1 for r in recipes if ing in r)

print(f'Part 1: {part1}')

# Part 2

final_allergens = dict()
queue = [x for x in possible_allergens if len(possible_allergens[x]) == 1]

while queue:
    allg = queue.pop(0)
    ing = possible_allergens[allg].pop()

    final_allergens[allg] = ing

    possible_allergens.pop(allg)
    for x in possible_allergens:
        if ing in possible_allergens[x]:
            possible_allergens[x].remove(ing)

    queue = [x for x in possible_allergens if len(possible_allergens[x]) == 1]

# generate the part2 output, ingredients sorted by allergen name
part2 = ','.join([final_allergens[x] for x in sorted(final_allergens)])
print('Part 2:', part2)
