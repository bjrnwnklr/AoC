from collections import defaultdict

f_name = 'input.txt'
# f_name = 'ex1.txt'

pos_dict = defaultdict(int)
with open(f_name, 'r') as f:
    for line in f.readlines():
        for i, c in enumerate(line.strip('\n')):
            pos_dict[(i, c)] += 1


for i in range(8):
    temp_dict = {k[1]: v for k, v in pos_dict.items() if k[0] == i}
    most_frequent = sorted(temp_dict, key=temp_dict.get, reverse=True)[-1]
    print(most_frequent, end='')

# part 1: mlncjgdg
# part 2: bipjaytb
