from collections import deque

f_name = 'input.txt'
n = 256
circle = deque(range(n))

with open(f_name, 'r') as f:
    inp_lengths = [int(x) for x in f.readline().strip('\n').split(',')]

curr_pos = 0
skip_size = 0

for inp_length in inp_lengths:
    # use deque rotate, popleft and extendleft (will add in reverse order)
    # pop off inp_length elements
    to_be_reversed = []
    i = inp_length
    while i > 0:
        to_be_reversed.append(circle.popleft())
        i -= 1
    # print(f'1. {list(circle)}, curr_pos: {curr_pos}, skip_size: {skip_size}.')

    # insert reverse of popped off elements
    circle.extendleft(to_be_reversed)
    # print(f'2. {list(circle)}, curr_pos: {curr_pos}, skip_size: {skip_size}.')

    # move by inp_length and skip_size
    circle.rotate(-1 * (inp_length + skip_size))
    # print(f'3. {list(circle)}, curr_pos: {curr_pos}, skip_size: {skip_size}.')
    
    # remember how many steps we moved i.e. where we are currently...
    curr_pos = (curr_pos + inp_length + skip_size) % n
    # print(f'4. {list(circle)}, curr_pos: {curr_pos}, skip_size: {skip_size}.')


    # increase skip_size by 1
    skip_size += 1

# we're done, now go back to the first list element (rotate back by -curr_pos)
circle.rotate(curr_pos)

print(list(circle))
print(f'Part 1: {circle[0] * circle[1]}.')

# Part 1: 29240

