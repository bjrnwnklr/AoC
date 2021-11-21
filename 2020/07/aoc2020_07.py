import re
from collections import defaultdict

f_name = 'input.txt'
# f_name = 'ex1.txt'

rules = defaultdict(list)
contained_in = defaultdict(list)
with open(f_name, 'r') as f:
    for line in f.readlines():
        # split at the "bags contain" to get the first and second parts
        left, right = line.strip('\n').split(' bags contain ')
        # first check if no other bags
        if right == 'no other bags.':
            rules[left] = []
        # split right side into individual bags
        else:
            # find all number + bag occurences
            matches = re.findall(r'((\d)\s(\w+\s\w+))', right)
            if matches:
                for m in matches:
                    rules[left].append((int(m[1]), m[2]))
                    contained_in[m[2]].append(left)

# now walk through the bags that can contain my shiny gold bag:
seen = set()
my_bag = 'shiny gold'
q = [my_bag]
while q:
    current_bag = q.pop()
    if current_bag in seen:
        continue

    seen.add(current_bag)
    for next_bag in contained_in[current_bag]:
        if next_bag not in seen:
            q.append(next_bag)

part1 = seen - {my_bag}
print(part1)
print(f'Part 1: Number of bags that can contain at least one shiny gold bag: {len(part1)}.')


# Part 1: 233

# For part 2, we need to traverse the graph in the other direction,
# starting from the shiny gold bag

def bag_contains(bag):
    if not rules[bag]:
        # we found the end point, return 1
        return 0
    else:
        temp_sum = 0
        for c, b in rules[bag]:
            temp_sum += c + c * bag_contains(b)
        return temp_sum
        # return sum(c * bag_contains(b) for c, b in rules[bag])

part2 = bag_contains(my_bag)

print(f'Part 2: {part2}')

# Part 2: 421550