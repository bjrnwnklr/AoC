import math

input = 368078


n = 21

def next_square(n):
    root = math.ceil(math.sqrt(n))
    if root % 2 == 0:
        root += 1
    return root

length = next_square(n)

# mid = length ** 2 - ((length - 1) // 2)
mid = length ** 2

dist = abs(mid - n) % length

print('n: ', n)
print('length: ', length)
print('mid: ', mid)
print('dist: ', dist)