# read input

input = open('input.txt', 'r').readline().strip()

ex1 = '1122'
ex2 = '1111'
ex3 = '1234'
ex4 = '91212129'

ex = ['1212', '1221', '123425', '123123', '12131415']

def captcha(inp, offset):
    l = len(inp)
    return sum(int(n) for i, n in enumerate(inp) if n == inp[(i + offset) % l])


inp = input

# part 1
offset = 1
print('Part 1: ', captcha(inp, 1))

offset = len(inp) // 2
print('Part 2: ', captcha(inp, offset))