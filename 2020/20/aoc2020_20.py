import math
import re
from collections import defaultdict
import numpy as np


def get_tile_checksum(t):
    """
    This uses two squares as the image representations:

    Original orientation        Same, but horizontally flipped with sides
        Side: 0                             >
       --->                                 4
      --------                         ^ 7     5 v
     ^| 0   1 ||                            6
    3||       || 1                          <
     ||       |v
      | 3    2|
      ---------
       <-----
          2
    """

    checksum = []
    # orig, upper (1-0)
    checksum.append(int(''.join([str(x) for x in t[0]]), 2))
    # orig, right (2-1)
    checksum.append(int(''.join([str(row[-1]) for row in t]), 2))
    # orig, bottom (3-2)
    checksum.append(int(''.join([str(x) for x in t[-1][::-1]]), 2))
    # orig, left (0-3)
    checksum.append(int(''.join([str(row[0]) for row in t[::-1]]), 2))

    # horiz flipped, upper (2-3)
    checksum.append(int(''.join([str(x) for x in t[-1]]), 2))
    # horiz flipped, right (1-2)
    checksum.append(int(''.join([str(row[-1]) for row in t[::-1]]), 2))
    # horiz flipped, bottom (0-1)
    checksum.append(int(''.join([str(x) for x in t[0][::-1]]), 2))
    # horiz flipped, left (3-0)
    checksum.append(int(''.join([str(row[0]) for row in t]), 2))

    checksum_matching = [checksum[i] for i in [6, 5, 4, 7, 2, 1, 0, 3]]

    return checksum, checksum_matching


# f_name = 'ex1.txt'
f_name = 'input.txt'

tile_dict = dict()

with open(f_name, 'r') as f:
    raw_tiles = f.read().strip().split('\n\n')

    for rt in raw_tiles:
        lines = rt.split('\n')
        tile_id = int(lines[0][4:9])
        tile = []
        for line in lines[1:]:
            tile.append([1 if x == '#' else 0 for x in line.strip()])

        tile_dict[tile_id] = tile

# generate three dictionaries:
# - per tile: checksum per side: 8 checksums per tile (4 for original tile, 4 for horizontally flipped tile)
# - per tile: matching checksum per side: which checksum connects to which checksum (side to side)
# - per checksum: sides per checksum - which (tile, side) connect to each checksum

checksum_per_side = defaultdict(list)
matching_checksums = dict()
sides_per_checksum = defaultdict(list)
for tile in tile_dict:
    checksum, checksum_matching = get_tile_checksum(tile_dict[tile])
    checksum_per_side[tile] = checksum
    for m, c in zip(checksum_matching, checksum):
        matching_checksums[m] = c

    for side, c in enumerate(checksum_per_side[tile]):
        sides_per_checksum[c].append((tile, side))

print('Checksum_per_side:')
for t, c in checksum_per_side.items():
    print(f'{t}: {c}')

print()
print('Matching_checksums:')
for m, c in matching_checksums.items():
    print(f'{m}: {c}')

print()
print('Sides_per_checksum:')
for c in sides_per_checksum:
    print(f'{c}: {sides_per_checksum[c]}')

# generate a dict that lists the matching sides for each side (tile, side): {(tile, side)}
matching_sides = dict()
for c in sides_per_checksum:
    for tile, side in sides_per_checksum[c]:
        m = matching_checksums[c]
        # find all sides that have a matching checksum but not the same as our current tile
        matches = [x for x in sides_per_checksum[m] if tile != x[0]]
        for x in matches:
            matching_sides[(tile, side)] = x

print()
print('Matching_sides:')
for t, s in sorted(matching_sides):
    print(f'({t}, {s}): {matching_sides[(t, s)]}')

# find number of unique tiles each tile is matching
unique_tile_matches = defaultdict(set)
for tile, side in matching_sides:
    t, _ = matching_sides[(tile, side)]
    unique_tile_matches[tile].add(t)

print()
print('unique_tile_matches:')
for t in unique_tile_matches:
    print(f'({t}): {unique_tile_matches[t]}')

print()
print('Corners:')
# print all tiles that have 2 matches (potential corners):
part1 = 1
corners = [t for t in unique_tile_matches if len(unique_tile_matches[t]) == 2]
for x in corners:
    print(x, [(ts, matching_sides[ts]) for ts in sorted(matching_sides) if ts[0] == x])
    part1 *= x

print(f'Part 1: {part1}')

# Part 1: 13224049461431


print()
print('Assembling the image.')

# To assemble the image:
# - find dimensions of grid (square root of number of tiles)
# - pick one corner tile and use it as the top left tile
# - rotate it until connecting pieces are at bottom and right
# - fill the top row by selecting tiles connecting to the one to the left. Rotate / flip until aligned
# - fill the first column by selecting tiles connecting to the one to the top. Rotate / flip until aligned
# - fill the rest row by row by selecting tiles that connect to the top and left. Rotate / flip to align
# Data structures needed:
# - grid that stores the tile IDs of the puzzle
# - dictionary[tile_id] to store the aligned (rotated/flipped) tiles as numpy array

# dimensions of grid
gridsize = int(math.sqrt(len(tile_dict)))
print(f'Gridsize: {gridsize}')

# pick the corner tile that has 1/2 as connecting sides (1 - right, 2 - bottom)
# we don't need to rotate or flip that tile then!
for x in corners:
    if (x, 1) in matching_sides and (x, 2) in matching_sides:
        print(f'Selected corner {x} with connecting sides 1 and 2')
        top_left_corner = x

# data structures
image_grid = []
aligned_tiles = dict()
# opposite sides - use to find the opposing side in a tile
# e.g. if the left side connects from side 0, then the right side is 2 and we need to look
# for the next tile connecting to the checksum on side 2
opp_sides = {
    0: 2,
    1: 3,
    2: 0,
    3: 1,
    4: 6,
    5: 7,
    6: 4,
    7: 5
}
# similar, find the bottom side if side 0 is right. This is used to store the bottom side,
# to which the next row down needs to connect each tile.
bottom_side = {
    0: 1,
    1: 2,
    2: 3,
    3: 0,
    4: 5,
    5: 6,
    6: 7,
    7: 4
}

# fill the top row and record which side is the bottom connecting side

top_row = [top_left_corner]
aligned_tiles[top_left_corner] = np.array(tile_dict[top_left_corner], int)
connecting_side = 1
bottom_connecting = [bottom_side[connecting_side]]
for i in range(1, gridsize):
    # pick the next tile and connecting side
    prev_tile = top_row[-1]
    next_tile, side = matching_sides[(prev_tile, connecting_side)]
    # rotate or flip based on matching side
    # connecting side needs to be 3 (for original tile) or 7 (for hflipped tile). Otherwise rotate / flip until aligned
    np_tile = np.array(tile_dict[next_tile], int)
    # flip if side is in [4:7]
    if side in [4, 5, 6, 7]:
        np_tile = np.flipud(np_tile)
    # rotate the tile (side + 1) % 4 (this makes side 3 or 7 to the left)
    np_tile = np.rot90(np_tile, (side + 1) % 4)
    # add the tile to the top row and store the aligned tile
    top_row.append(next_tile)
    aligned_tiles[next_tile] = np_tile.copy()
    # update the connecting side to the opposite of the current side
    connecting_side = opp_sides[side]
    # store which side is connected to the bottom
    bottom_connecting.append(bottom_side[connecting_side])

image_grid.append(top_row)

print()
print('Top row:')
for t in top_row:
    print(t)
    print(aligned_tiles[t])

# fill the rest of the rows
for row in range(1, gridsize):
    # get the tile on top
    prev_row = image_grid[row - 1]
    new_row = []
    for col in range(gridsize):
        prev_tile = prev_row[col]
        connecting_side = bottom_connecting[col]
        # pick the next tile and connecting side
        next_tile, side = matching_sides[(prev_tile, connecting_side)]
        np_tile = np.array(tile_dict[next_tile], int)
        # flip if side is in [4:7]
        if side in [4, 5, 6, 7]:
            np_tile = np.flipud(np_tile)
        # rotate the tile (side + 1) % 4 (this makes side 3 or 7 to the left)
        np_tile = np.rot90(np_tile, side % 4)
        new_row.append(next_tile)
        aligned_tiles[next_tile] = np_tile.copy()
        # update the bottom connecting side to the opposite of the top side
        bottom_connecting[col] = opp_sides[side]
    image_grid.append(new_row)

print()
print('Finished image:')
for i, row in enumerate(image_grid):
    print(f'Row {i}:')
    for t in row:
        print(t)
        print(aligned_tiles[t])

print()
print('Image tiles:')
for row in image_grid:
    print(row)

# now create a representation of the image:
# - strip the borders from each tile
# - assemble a np array from all resulting tiles
final_tiles = dict()
for row in image_grid:
    for t in row:
        temp_tile = aligned_tiles[t][1:-1, 1:-1].copy()
        final_tiles[t] = temp_tile

print()
print('Final reshaped tiles:')
for i, row in enumerate(image_grid):
    print(f'Row {i}:')
    for t in row:
        print(t)
        print(final_tiles[t])

# stack the tiles per row
image_rows = []
for row in image_grid:
    new_row = np.hstack([final_tiles[t] for t in row])
    image_rows.append(new_row)

final_image = np.vstack(image_rows)

print()
print('Final image:')
print(final_image)


# get string representation and prettify image (replace 0 with '.' and '1' with '#'
def pretty_image(nparr):
    img = []
    for row in nparr:
        img.append(''.join('#' if c == 1 else '.' for c in row))
    return img

def print_image(img):
    for row in img:
        print(row)

img_to_print = pretty_image(final_image)
print()
print('Final image in pretty:')
print_image(img_to_print)

regex_1 = re.compile(r'[.#]{18}#')
regex_2 = re.compile(r'#(?:[.#]{4}##){3}#')
regex_3 = re.compile(r'[.#](?:#[.#]{2}){5}#')

# go through each variant of the image (rotated and flipped) and look for sea monster patterns
monster_count = 0
for rot in [0, 1, 2, 3]:
    for flip in [False, True]:
        found = False
        test_image = final_image.copy()
        if flip:
            test_image = np.flipud(test_image)
        test_image = np.rot90(test_image, rot)
        pretty_test_image = pretty_image(test_image)
        pretty_test_image_w_monsters = pretty_image(test_image)

        # find the 2nd pattern
        for i in range(1, len(pretty_test_image)):
            # use finditer since we need to find all occurrences in one line (search only returns the FIRST match
            # per line so might not catch another match later in the line)
            match_line2 = regex_2.finditer(pretty_test_image[i])
            if match_line2:
                for m in match_line2:
                    print(m)
                    line2_start = m.start()
                    # try to match the 3rd group at the same position. 3rd pattern is 17 chars long
                    match_line3 = regex_3.match(pretty_test_image[i + 1][line2_start:line2_start + 17])
                    if match_line3:
                        # now try to find the 1st pattern in the line above. 1st pattern is 19 chars long
                        match_line1 = regex_1.match(pretty_test_image[i - 1][line2_start:line2_start + 19])
                        if match_line1:
                            # we found a sea monster!
                            print()
                            print(f'Found sea monster! Image rotation: {rot}, flip: {flip}. Loc: {i}:{line2_start}')
                            # print_image(pretty_test_image)
                            monster_count += 1
                            found = True

                            # insert the monster image at the position
                            monster_pixel_pos = [
                                (i - 1, [18]),
                                (i, [0, 5, 6, 11, 12, 17, 18, 19]),
                                (i + 1, [1, 4, 7, 10, 13, 16])
                            ]
                            for r, cols in monster_pixel_pos:
                                temp_row = [p for p in pretty_test_image_w_monsters[r]]
                                for c in cols:
                                    temp_row[c + line2_start] = 'O'
                                pretty_test_image_w_monsters[r] = ''.join(temp_row)

        if found:
            print()
            print('Image w/out monsters:')
            print_image(pretty_test_image)
            print()
            print('Image w/ monsters:')
            print_image(pretty_test_image_w_monsters)

print()
print(f'Found {monster_count} monsters.')

# each monster has 15 #s. Count the number of 1s in the image and remove monster_count * 15
# the image rotation is not important here.

number_of_water_tiles = np.sum(final_image)
part2 = number_of_water_tiles - 15 * monster_count
print()
print(f'Part 2: {part2}')

# Part 2: 2231
