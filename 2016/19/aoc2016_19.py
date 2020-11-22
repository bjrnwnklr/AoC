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


