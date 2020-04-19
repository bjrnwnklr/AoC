from collections import defaultdict

input_string = open(r'D:\Python\Advent\5.1\input.txt', 'r').read().strip()


letters = {ch.lower() for ch in input_string}

def resolve(input_string):
    stack = []
    for ch in input_string:
        if stack and stack[-1] == ch.swapcase():
            stack.pop()
        else:
            stack.append(ch)
    return(len(stack))

part1 = resolve(input_string)
print('Part 1: %d' % (part1))


length = defaultdict(int)

for l in letters:
    test_string = input_string.replace(l, '')
    test_string = test_string.replace(l.upper(), '')
    length[l] = resolve(test_string)

part2 = min(length, key=length.get)
print('Part 2: %s, %d' % (part2, length[part2]))