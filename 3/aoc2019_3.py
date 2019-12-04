# read in input
# each line is one wire, each comma separated value is one instruction

wire = []
with open('input.txt') as f:
    wire = [[(i[:1], int(i[1:])) for i in line.strip('\n').split(',')] for line in f.readlines()]

grid = []
cp = (0, 0)

dir_tup = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}



#wire = [[('R', 8),('U', 5),('L', 5),('D', 3)], [('U', 7),('R', 6),('D', 4),('L', 4)]]

for w in wire:
    g = set()
    current = cp
    for d, c in w:
        g.update(set((current[0] + j * dir_tup[d][0], current[1] + j * dir_tup[d][1]) for j in range(1, c + 1)))
        current = (current[0] + c * dir_tup[d][0], current[1] + c * dir_tup[d][1])

    grid.append(g)

# get intersection between wires - all points where they cross
intersect = grid[0] & grid[1]
print('Wires crossing at: ', intersect)

# Every point's distance to the central point is just the sum of the row and column
closest = sorted(intersect, key=lambda x: abs(x[0]) + abs(x[1]))[0]

print('Closest: {}, distance: {}'.format(closest, abs(closest[0]) + abs(closest[1])))

# correct answer part 1: 293

###### part 2
# This time, use a list and not a set for the path
# Then, get the index in the list for each intersection and add up the two indices

grid_2 = []

for w in wire:
    g = [(0, 0)]
    current = cp
    for d, c in w:
        g.extend([(current[0] + j * dir_tup[d][0], current[1] + j * dir_tup[d][1]) for j in range(1, c + 1)])
        current = (current[0] + c * dir_tup[d][0], current[1] + c * dir_tup[d][1])

    grid_2.append(g)

# print(grid_2[0])

# get index for each intersection and add to dictionary
intersect_distance = {i: grid_2[0].index(i) + grid_2[1].index(i) for i in intersect}

print(intersect_distance)

part2_key = sorted(intersect_distance, key=intersect_distance.get)[0]

print('Part 2: closest intersection distance is ', intersect_distance[part2_key])

# correct answer is 27306 (intersection at (301, -821))

