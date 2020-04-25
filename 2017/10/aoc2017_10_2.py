from collections import deque
import operator
import functools

f_name = 'input.txt'
n = 256
circle = deque(range(n))

with open(f_name, 'r') as f:
    inp_lengths = f.readline().strip('\n').strip(' ')


# convert to ascii codes - each character
ascii_lengths = [ord(x) for x in inp_lengths]
# extend with end sequence given
ascii_lengths += [17, 31, 73, 47, 23]

curr_pos = 0
skip_size = 0
cycles = 64

# run 64 times
for _ in range(cycles):
    for inp_length in ascii_lengths:
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

# now create the the dense hash
dense_hash = []
for j in range(16):
    # perform bitwise xor on each block of 16
    block = list(circle)[j*16:(j+1)*16]
    
    dense_hash.append(functools.reduce(operator.__xor__, block))

# create hexadecimal string representation
hexa_string = ''.join(f'{x:02x}' for x in dense_hash)

print(f'Part 2: {hexa_string}')

# Part 1: 29240
# Part 2: 4db3799145278dc9f73dcdbc680bd53d
