
inp = '10111100110001111'

ex1 = '10000'
disk = 20

def f_dragon(n, a):
    if len(a) >= n:
        return a[:n]
    else:
        # reverse the order
        b = a[::-1]
        # reverse
        b = ''.join(['0' if x == '1' else '1' for x in b])
        # call function recursively with new input
        return f_dragon(n, a + '0' + b)

def checksum(a):
    b = ''.join(['1' if a[i] == a[i+1] else '0' for i in range(0, len(a), 2)])
    if len(b) % 2 == 0:
        return checksum(b)
    else:
        return b

# print(checksum(f_dragon(disk, ex1)))
print(checksum(f_dragon(272, inp)))

# part 1: 11100110111101110
print(checksum(f_dragon(35651584, inp)))

# part 2: 10001101010000101