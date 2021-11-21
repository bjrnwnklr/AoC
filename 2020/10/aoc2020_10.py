from collections import defaultdict
from functools import lru_cache

# f_name = 'ex1.txt'
# f_name = 'ex2.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    adapters = [int(x.strip('\n')) for x in f.readlines()]

# Find largest adapter to determine built in adapter joltage
built_in = max(adapters) + 3
# add in the built in joltage, then sort ascending
adapters = sorted(adapters + [built_in])
current_joltage = 0
distribution = defaultdict(int)

for a in adapters:
    # get first joltage and see if we can add it to the current_joltage
    delta = a - current_joltage
    if 1 <= delta <= 3:
        distribution[delta] += 1
    else:
        print(f'{a} does not fit on {current_joltage}!')
        break

    # update current_joltage
    current_joltage = a

print(f'Done! Distribution: {distribution}')
print(f'Part 1: {distribution[1] * distribution[3]}.')


# Part 1: 1656

# Part 2, recursive with memoization
@lru_cache
def sum_of_child_nodes(node):
    if not children[node]:
        return 1
    else:
        return sum(sum_of_child_nodes(n) for n in children[node])


# build a graph, then traverse it to calculate the number of possible combinations under each node
children = defaultdict(list)

for a in adapters + [0]:
    for i in range(1, 4):
        check_val = a + i
        if check_val in adapters:
            children[a] += [check_val]

part2 = sum_of_child_nodes(0)
print(f'Part 2: {part2}')

# Part 2: 56693912375296

# Part 2, dynamic programming

paths_to = defaultdict(int, {0: 1})
all_adapters_sorted = sorted(adapters)

for a in all_adapters_sorted:
    paths_to[a] = paths_to[a - 1] + paths_to[a - 2] + paths_to[a - 3]

print(f'Part 2, dp: {paths_to[all_adapters_sorted[-1]]}')
