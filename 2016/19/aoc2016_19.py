from collections import deque

# number of elves
# elves = 5
elves = 3012210

# create a circle of elves (indexes to our dictionary of elves)
circle = deque(range(1, elves + 1))
presents = {k: 1 for k in range(1, elves + 1)}

# repeat until the circle only has one element
while len(circle) > 1:
    # add presents from next elf to current elf
    presents[circle[0]] += presents[circle[1]]
    # remove presents from next elf
    presents[circle[1]] = 0

    # rotate to next elf
    circle.rotate(-1)
    # remove next elf as they have no present
    circle.popleft()

print(circle[0], presents[circle[0]])

# Part 1: 1830117

# ----- Part 2 -------

# create two half circles of elves
mid = elves // 2
h1 = deque(range(1, mid + 1))
h2 = deque(range(mid + 1, elves + 1))

# repeat until the circle only has one element
while len(h1) + len(h2) > 1:
    # remove the first element of the 2nd half - the elf opposite of the current position
    h2.popleft()
    # move the current elf to the end of the 2nd half queue
    h2.append(h1.popleft())
    # if the overall length is odd, we also need to move the start of h2 to the end of h1 to balance
    if (len(h1) + len(h2)) % 2 == 0:
        h1.append(h2.popleft())

if h1:
    print(f'h1: {h1[0]}')
if h2:
    print(f'h2: {h2[0]}')

# Part 2: 1417887