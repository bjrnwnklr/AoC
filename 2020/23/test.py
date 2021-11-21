from collections import deque

d = deque([1, 2, 3, 4, 5])
l = [6, 7, 8]


curr_cup = d[0]
# insert l after 2
dest_cup_idx = d.index(4)
print(f'{dest_cup_idx=}')

d.rotate(-dest_cup_idx - 1)
print(f'{d=}')

d.extend(l)
print(f'{d=}')

# rotate back to current cup + 1
# curr_cup_index = d.index(curr_cup)
# d.rotate(-curr_cup_index - 1)
d.rotate(dest_cup_idx + 3)
print(f'{d=}')