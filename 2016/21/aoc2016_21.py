import re

password = 'abcdefgh'
# password = 'abcde'
temp_pw = list(password)

f_name = 'input.txt'
# f_name = 'ex1.txt'

with open(f_name, 'r') as f:
    for line in f.readlines():
        if line.startswith('swap position'):
            x, y = map(int, re.findall(r'(\d+)', line))

            tmp_y = temp_pw[y]
            tmp_x = temp_pw[x]
            temp_pw[x] = tmp_y
            temp_pw[y] = tmp_x

            print(f'swap position {x}, {y}')

        elif line.startswith('swap letter'):
            x = line.split(' ')[2]
            y = line.split(' ')[5].strip('\n')

            x_index = temp_pw.index(x)
            y_index = temp_pw.index(y)

            temp_pw[x_index] = y
            temp_pw[y_index] = x

            print(f'swap letter {x}, {y}')

        elif line.startswith(('rotate left', 'rotate right')):
            x, = map(int, re.findall(r'(\d+)', line))

            if 'left' in line:
                temp_pw = temp_pw[x:] + temp_pw[:x]

                print(f'rotate left {x}')
            else:
                temp_pw = temp_pw[-x:] + temp_pw[:-x]
                print(f'rotate right {x}')

        elif line.startswith('rotate based'):
            x = line.strip('\n')[-1]

            x_index = temp_pw.index(x)
            rots = 1 + x_index
            if x_index >= 4:
                rots += 1
            # account for the case where the number of rotations is longer than the length of the password
            rots %= len(password)
            temp_pw = temp_pw[-rots:] + temp_pw[:-rots]

            print(f'rotate based on pos of {x}')

        elif line.startswith('reverse positions'):
            x, y = map(int, re.findall(r'(\d+)', line))

            # reversing a string only works if the 2nd index (to count down to) is >= 0
            # if it has to include the index at 0, it needs to be replaced with '' in the [y+1::-1] list slice
            mid = temp_pw[y:x-1:-1] if x > 0 else temp_pw[y::-1]
            temp_pw = temp_pw[:x] + mid + temp_pw[y+1:]

            print(f'reverse positions {x}, {y}')

        elif line.startswith('move position'):
            x, y = map(int, re.findall(r'(\d+)', line))

            # remove the letter found at pos x
            tmp_x = temp_pw[x]
            temp_pw = temp_pw[:x] + temp_pw[x+1:]
            temp_pw.insert(y, tmp_x)

            print(f'move position {x}, {y}')
        print(''.join(temp_pw))

    password = ''.join(temp_pw)
    print(f'Part 1: Password is {password}')

    # Part 1: dgfaehcb

    # Part 2:
    # - go through lines in reverse
    # Operations:
    # - Swap position: works the same
    # - Swap letter: works the same
    # - rotate left / right: direction needs to be reversed
    # - rotate based on pos: hmmm
    # - reverse positions: works the same
    # - move pos: needs to be reversed

    password_pt2 = 'fbgdceah'
    # password_pt2 = 'decab'
    # password_pt2 = 'dgfaehcb'
    temp_pw = list(password_pt2)
    with open(f_name, 'r') as f:
        for line in f.readlines()[::-1]:
            if line.startswith('swap position'):
                x, y = map(int, re.findall(r'(\d+)', line))

                tmp_y = temp_pw[y]
                tmp_x = temp_pw[x]
                temp_pw[x] = tmp_y
                temp_pw[y] = tmp_x

                print(f'swap position {x}, {y}')

            elif line.startswith('swap letter'):
                x = line.split(' ')[2]
                y = line.split(' ')[5].strip('\n')

                x_index = temp_pw.index(x)
                y_index = temp_pw.index(y)

                temp_pw[x_index] = y
                temp_pw[y_index] = x

                print(f'swap letter {x}, {y}')

            elif line.startswith(('rotate left', 'rotate right')):
                x, = map(int, re.findall(r'(\d+)', line))

                if 'left' in line:
                    temp_pw = temp_pw[-x:] + temp_pw[:-x]

                    print(f'rotate left {x}')
                else:
                    temp_pw = temp_pw[x:] + temp_pw[:x]
                    print(f'rotate right {x}')

            elif line.startswith('rotate based'):
                # we can derive the original position based on the current position:
                # pos   shift   new pos
                # 0     1       1
                # 1     2       3
                # 2     3       5
                # 3     4       7
                # 4     6       2
                # 5     7       4
                # 6     8       6
                # 7     9       0
                # calculate a dictionary with lookup for each index
                rot_dict = dict()
                pw_length = len(password)
                for i in range(8):
                    shift = i + 1 if i < 4 else i + 2
                    new_pos = (i + shift) % pw_length
                    rot_dict[new_pos] = shift % pw_length

                x = line.strip('\n')[-1]
                x_index = temp_pw.index(x)

                # get the number of reverse rotations required to reverse the rotation
                rev_rots = -rot_dict[x_index]
                temp_pw = temp_pw[-rev_rots:] + temp_pw[:-rev_rots]

                print(f'rotate based on pos of {x}')

            elif line.startswith('reverse positions'):
                x, y = map(int, re.findall(r'(\d+)', line))

                # reversing a string only works if the 2nd index (to count down to) is >= 0
                # if it has to include the index at 0, it needs to be replaced with '' in the [y+1::-1] list slice
                mid = temp_pw[y:x - 1:-1] if x > 0 else temp_pw[y::-1]
                temp_pw = temp_pw[:x] + mid + temp_pw[y + 1:]

                print(f'reverse positions {x}, {y}')

            elif line.startswith('move position'):
                x, y = map(int, re.findall(r'(\d+)', line))

                # remove the letter found at pos x
                tmp_y = temp_pw[y]
                temp_pw = temp_pw[:y] + temp_pw[y + 1:]
                temp_pw.insert(x, tmp_y)

                print(f'move position {x}, {y}')
            print(''.join(temp_pw))

        password = ''.join(temp_pw)
        print(f'Part 2: Password is {password}')

        # Part 2: fdhgacbe
