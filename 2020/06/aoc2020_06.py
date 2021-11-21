from collections import Counter

f_name = 'input.txt'
# f_name = 'ex1.txt'

with open(f_name, 'r') as f:
    groups = [p for p in f.read().split('\n\n')]

part1 = 0
for g in groups:
    c = Counter(g.replace('\n', ''))
    part1 += len(c)

print(f'Part 1: sum of questions: {part1} ')

# Part 1: 6457
part2 = 0
for g in groups:
    counter = Counter()
    answers = g.strip().split('\n')
    groupsize = len(answers)

    for a in answers:
        counter += Counter(list(a))

    part2 += sum(1 for c in counter if counter[c] == groupsize)

print(part2)

# Part 2: 3260