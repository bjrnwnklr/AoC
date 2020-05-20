

f_name = 'input.txt'
# f_name = 'ex1.txt'

curr_pos = (0, 0)
curr_dir = 0
# directions = north, east, south, west - 0, 1, 2, 3
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

visited = set()

with open(f_name, 'r') as f:
    line = f.readline().strip('\n')
    for instruction in line.split(', '):
        turn = 1 if instruction.strip()[0] == 'R' else -1
        blocks = int(instruction.strip()[1:])
        curr_dir = (curr_dir + turn) % 4
        for _ in range(blocks):
            curr_pos = (curr_pos[0] + directions[curr_dir][0], curr_pos[1] + directions[curr_dir][1])
            if curr_pos in visited:
                print(f'Visited {curr_pos} twice. Distance is {sum(abs(x) for x in curr_pos)}')
            visited.add(curr_pos)

# we're done
print(f'End point: {curr_pos}')
print(sum(abs(x) for x in curr_pos))

# part 1: 161
# part 2: 110 (14, -96)