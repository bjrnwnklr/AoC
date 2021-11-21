# f_name = 'ex1.txt'
f_name = 'input.txt'

with open(f_name, 'r') as f:
    instructions = [(line[0], int(line[1:].strip('\n'))) for line in f.readlines()]

direction_moves = {
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1),
    'N': (-1, 0)
}

directions = [
    'E',
    'S',
    'W',
    'N'
]

pos = (0, 0)
curr_dir = 0 # 0 = East

for action, val in instructions:
    if action in direction_moves or action == 'F':
        if action == 'F':
            move_in = direction_moves[directions[curr_dir]]
        else:
            move_in = direction_moves[action]
        pos = (pos[0] + move_in[0] * val, pos[1] + move_in[1] * val)
    else:
        # calculate turning in direction
        # L means moving backwards in directions index, R means moving forwards in direction index
        # degrees are all multiples of 90, so mean 90 = move 1 index, etc
        # use modulo to determine new direction
        i = val // 90
        sign = 1 if action == 'R' else -1
        curr_dir = (curr_dir + sign * i) % 4

print(f'Position is {pos}, facing {directions[curr_dir]}. Manhattan distance {abs(pos[0]) + abs(pos[1])}.')

# Part 1 with complex numbers
complex_moves = {
    'E': complex(1, 0),
    'S': complex(0, -1),
    'W': complex(-1, 0),
    'N': complex(0, 1)
}

pos = complex(0, 0)
curr_dir = complex(1, 0)

for action, val in instructions:
    if action in complex_moves:
        pos += complex_moves[action] * val
    elif action == 'F':
        pos += curr_dir * val
    else:
        i = val // 90
        sign = -1j if action == 'R' else 1j
        for _ in range(i):
            curr_dir *= sign

print(f'Position is {pos}, facing {curr_dir}. Manhattan distance {int(abs(pos.real) + abs(pos.imag))}.')

# Part 1: 962

# Part 2 with complex numbers
# complex numbers: real part is the columns (positive is right/east), imag part is the rows (positive is up/north)

pos = complex(0, 0)
# wp is 10 units east and 1 unit north
wp = complex(10, 1)

complex_moves = {
    'E': complex(1, 0),
    'S': complex(0, -1),
    'W': complex(-1, 0),
    'N': complex(0, 1)
}

for action, val in instructions:
    if action in complex_moves:
        # move the waypoint
        wp += complex_moves[action] * val
    elif action == 'F':
        # move the ship in the direction of the waypoint
        pos += wp * val
    else:
        # rotate the waypoint multiple times to get to right rotation
        i = val // 90
        sign = -1j if action == 'R' else 1j
        for _ in range(i):
            wp *= sign

# print out result
print(f'Final position of ship is {pos}. Manhattan distance: {int(abs(pos.real) + abs(pos.imag))}.')

# Part 2: 56135
