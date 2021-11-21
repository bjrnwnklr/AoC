f_name = 'input.txt'


def decode_seat(bpass):
    row_part = bpass[:7]
    col_part = bpass[7:]

    row_pos = (0, 127)
    col_pos = (0, 7)

    for c in row_part:
        mid = (row_pos[1] - row_pos[0]) // 2
        if c == 'B':
            row_pos = (row_pos[0] + mid + 1, row_pos[1])
        else:
            row_pos = (row_pos[0], row_pos[0] + mid)

    for c in col_part:
        mid = (col_pos[1] - col_pos[0]) // 2
        if c == 'R':
            col_pos = (col_pos[0] + mid + 1, col_pos[1])
        else:
            col_pos = (col_pos[0], col_pos[0] + mid)

    return row_pos[0], col_pos[0], row_pos[0] * 8 + col_pos[0]


assert (decode_seat('FBFBBFFRLR') == (44, 5, 357))

seats = dict()
with open(f_name, 'r') as f:
    for bpass in f.readlines():
        seat = decode_seat(bpass.strip('\n'))
        seats[seat[2]] = (seat[0], seat[1])

# find highest ID in seats
max_seat = max(seats)

print(f'Part 1: highest seat ID: {max_seat}: {seats[max_seat]}')

# Part 1: 801

# find lowest and highest ID (highest we already have), then range through them and check if +1 and -1 are in the list

min_seat = min(seats)

for s in range(min_seat, max_seat):
    if s not in seats and s-1 in seats and s+1 in seats:
        print(f'Part 2: Your seat is {s}, between seats {seats[s-1]} and {seats[s+1]}.')

# Part 2: Your seat is 597, between seats (74, 4) and (74, 6).
