

f_name = 'input.txt'
# f_name = 'ex1.txt'


keypad = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

curr_pos = (1, 1) # start at 5 button

moves = {
    'U': (-1, 0),
    'L': (0, -1),
    'D': (1, 0),
    'R': (0, 1)
}

with open(f_name, 'r') as f:
    # read in one line
    for line in f.readlines():
        for move in line.strip('\n'):
            new_pos = (curr_pos[0] + moves[move][0], curr_pos[1] + moves[move][1])
            if 0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3:
                curr_pos = new_pos
        button = keypad[curr_pos[0]][curr_pos[1]]
        print(button, end='')
    print('')

# part 1: 98575

keypad_2 = [
    [0, 0, 1, 0, 0],
    [0, 2, 3, 4, 0],
    [5, 6, 7, 8, 9],
    [0, 'A', 'B', 'C', 0],
    [0, 0, 'D', 0, 0]
]

curr_pos = (2, 0) # start at 5 in keypad_2

with open(f_name, 'r') as f:
    # read in one line
    for line in f.readlines():
        for move in line.strip('\n'):
            new_pos = (curr_pos[0] + moves[move][0], curr_pos[1] + moves[move][1])
            if 0 <= new_pos[0] < 5 and 0 <= new_pos[1] < 5 and keypad_2[new_pos[0]][new_pos[1]] != 0:
                curr_pos = new_pos
        button = keypad_2[curr_pos[0]][curr_pos[1]]
        print(button, end='')
    print('')

# part 2: CD8D4