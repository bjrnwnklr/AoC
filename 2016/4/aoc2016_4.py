import re
from collections import Counter

f_name = 'input.txt'
# f_name = 'ex1.txt'

re_room_name = r'([a-z]+)-'
re_full_room_name = r'(([a-z]+-)+)'
re_sector_id = r'(\d+)'
re_checksum = r'\[([a-z]+)\]'

real_sector_ids = []
real_rooms = []

with open(f_name, 'r') as f:
    for line in f.readlines():
        # store room name (including dashes) - for part 2
        full_name = re.match(re_full_room_name, line.strip('\n'))[0]
        # split the line for part 1, e.g. concat the letters extracted from the room name and feed to a Counter
        # to find the most common letters
        room_name = Counter(''.join(re.findall(re_room_name, line.strip('\n'))))
        sector_id = int(re.findall(re_sector_id, line.strip('\n'))[0])
        checksum = re.findall(re_checksum, line.strip('\n'))[0]

        # part 1: calculate the 5 most frequent letters by using a tuple of:
        # - the count of the letters (most frequent first - reverse = True (descending order))
        # - the ASCII code (negative since we want the lowest first while using descending order)
        calc_checksum = ''.join(
            sorted(
                room_name, 
                key=lambda x: (room_name[x], -ord(x)), 
                reverse=True)[:5]
        )

        if checksum == calc_checksum:
            real_sector_ids.append(sector_id)
            # add room to list of real rooms
            real_rooms.append((full_name, sector_id))

print(f'Part 1: Sum of sector IDs = {sum(real_sector_ids)}')

# Part 1: 361724

#### Part 2:

letters = 'abcdefghijklmnopqrstuvwxyz'

decrypted_words = set()

for room, sector in real_rooms:
    # rotate x number of times forward - this can be done modulo 26 as there are only 26 letters
    rotation = sector % 26
    # split the room into separate words
    words = room.rstrip('-').split('-')
    new_name = [''.join(letters[(letters.index(c) + rotation) % 26] for c in word) for word in words]
    for d_word in new_name:
        decrypted_words.add(d_word)
    if 'northpole' in new_name:
        print(f'Found NORTHPOLE: {new_name}. Sector: {sector}')

print(f'Found {len(decrypted_words)} words.')
print(decrypted_words)

# part 2: 482
