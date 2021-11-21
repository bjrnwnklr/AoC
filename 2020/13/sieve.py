# input_numbers = [7, 5, 11, 13]
# input_numbers = [67, 7, 59, 61]
# input_numbers = [67, 7, 'x', 59, 61]
f_name = 'ex1.txt'
# f_name = 'input.txt'

with open(f_name, 'r') as f:
    f.readline()
    input_numbers = [x.strip('\n') for x in f.readline().split(',')]

# generate the remainders
numbers = []
remainders = []
for i, n in enumerate(input_numbers):
    if n != 'x':
        n = int(n)
        numbers.append(n)
        remainders.append((n - i) % n)

print(numbers)
print(remainders)

x = remainders.pop(0)
n = numbers.pop(0)

for a_i, n_i in zip(remainders, numbers):
    i = 1
    while True:
        if (x + i * n) % n_i == a_i:
            x = x + i * n
            n *= n_i
            break
        i += 1
    print(f'a_i: {a_i}, n_i: {n_i}, x: {x}, n: {n}')

print(f'Solution: {x}')
