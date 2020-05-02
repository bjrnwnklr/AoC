from collections import deque
import operator
import functools


def knot_hash(inp_lengths):

    # convert to ascii codes - each character
    ascii_lengths = [ord(x) for x in inp_lengths]
    ascii_lengths += [17, 31, 73, 47, 23]
    
    n = 256
    circle = deque(range(n))
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

    return hexa_string


inp_lengths = 'hxtvlmkl'
# inp_lengths = 'flqrgnkx'

grid = []

p1_result = 0
for r in range(128):
    knot = int(knot_hash(inp_lengths + f'-{r}'), 16)
    bin_view = f'{knot:0128b}'
    grid.append(list(map(int, list(bin_view))))
    p1_result += sum(int(x) for x in list(bin_view))

print(f'Part 1: {p1_result}')

# Part 1: 8214

# part 2: find regions

# use a naive approach: 
# - start with the first 1 in the top row
# - run a BFS on each group- add to a queue until we don't find any more neighbors
# - keep a global "seen" list

seen = set()
regions = 0

# all used squares in one list. We need this full list to check if a neighbor is a used square
squares = [(r,c) for r in range(128) for c in range(128) if grid[r][c]]
# create a queue of squares to start with, we will pop off of this list
square_q = squares[:]
print(len(squares))

while square_q:
    # get the next square
    curr_sq = square_q.pop(0)

    # skip to next if we have already seen the square
    if curr_sq in seen:
        continue

    # we found a new group, so increase group count
    regions += 1

    # now run a mini bfs to find all connected squares
    q = deque([curr_sq])

    while q:
        # get next square
        region_square = q.popleft()

        if region_square in seen:
            continue

        # add to seen
        seen.add(region_square)

        # now add neighbors to the inner q
        for n in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            next_sq = (region_square[0] + n[0], region_square[1] + n[1])
            if next_sq in squares:
                q.append(next_sq)
        
print(f'Regions found: {regions}')

# Part 2: 1093
