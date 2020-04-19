import math

# part 1 - solution: 371
input = 368078


n = input

def next_square(n):
    root = math.ceil(math.sqrt(n))
    if root % 2 == 0:
        root += 1
    return root

# how long is the side of the square? Round up square root of the target number to next odd number
side_length = next_square(n)
# how far is the middle of the side from the corner?
side_mid = (side_length - 1) // 2

# number in the middle of the side with the highest number in the bottom right corner (e.g. 25 - mid = 23)
mid = side_length ** 2 - side_mid
# how far is the target number from the mid point of the side (modula side_length so it doesn't matter on which side)
dist = abs(mid - n) % (side_length - 1)

corner_offset = abs(dist - side_mid)

# max distance - from the corner
max_dist = side_length - 1

target_dist = max_dist - corner_offset

print('n: ', n)
print('length: ', side_length)
print('mid: ', mid)
print('dist: ', dist)
print('corner_offset: ', corner_offset)
print('max_dist: ', max_dist)
print('target_dist: ', target_dist)

# solution part 2: 369601 (lookup at https://oeis.org/A141481/b141481.txt)