from collections import deque

# our input
steps = 312
# steps = 3

buffer = deque([0])
cycles = 50_000_000

for i in range(1, cycles+1):
    buffer.rotate(-(steps+1))
    buffer.appendleft(i) 
    # if buffer[-1] == 0:
        # print(f'{i}\t{len(buffer)}\t{buffer[0]}, {buffer[-1]}')

zero_ind = buffer.index(0)
print(zero_ind, buffer[zero_ind], buffer[zero_ind + 1])
# Part 1: 772
# Part 2: 42729050


