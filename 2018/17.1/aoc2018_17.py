import re


def get_dims():
    # get dimensions from clay min and max
    min_x, max_x = min(clay, key=lambda x: x[0])[0], max(clay, key=lambda x: x[0])[0]
    min_y, max_y = min(clay, key=lambda x: x[1])[1], max(clay, key=lambda x: x[1])[1]
    return min_x, max_x, min_y, max_y


def print_map():
    min_x, max_x, min_y, max_y = get_dims()
    print('   ' + ''.join([str(i % 10) for i in range(min_x - 1, max_x + 2)]))
    for y in range(min_y - 6, max_y + 2):
        row = f'{y:04}'
        for x in range(min_x - 1, max_x + 2):
            if (x, y) in clay:
                c = '#'
            elif (x, y) == spring:
                c = '+'
            elif (x, y) in water_at_rest:
                c = '~'
            elif (x, y) in moving_water:
                c = '|'
            else:
                c = '.'
            row += c
        print(row)


def pour_water(x, y, water_at_rest, moving_water, water_flow_queue):
    # process a square of water by looking at the square below to decide what should be done
    next_square = (x, y + 1)
    # if below is flowing water, add to water_flow_queue
    if next_square not in clay and next_square not in moving_water and next_square not in water_at_rest:
        moving_water.add(next_square)
        water_flow_queue.append(next_square)
    elif next_square in clay or next_square in water_at_rest:
        # we found either clay or water at rest below, fill with either
        # water at rest (if walls to left and right), or with flowing water (if 0 or 1 walls)
        wall_left, x_left = find_walls(x, y, -1)
        wall_right, x_right = find_walls(x, y, 1)
        if wall_right and wall_left:
            # we have walls to both sides. Extend water at rest to both sides
            for delta_x in range(x_left, x_right + 1):
                water_at_rest.add((x + delta_x, y))
                if (x + delta_x, y) in moving_water:
                    moving_water.remove((x + delta_x, y))
            # and remove the current square from moving water
            # moving_water.remove((x, y))
            # add previous flowing water square to queue
            water_flow_queue.append((x, y - 1))
        else:
            # we don't have walls, extend flowing water to both sides
            for delta_x in range(x_left, x_right + 1):
                moving_water.add((x + delta_x, y))
            # add any flowing water below the drop to the queue to review
            if not wall_left:
                moving_water.add((x + x_left, y + 1))
                water_flow_queue.append((x + x_left, y + 1))
            if not wall_right:
                moving_water.add((x + x_right, y + 1))
                water_flow_queue.append((x + x_right, y + 1))



def find_walls(x, y, direction):
    delta_x = 0
    # print(f'Finding walls from ({x}, {y}), dir {direction}.')
    while (x + delta_x, y + 1) in clay or (x + delta_x, y + 1) in water_at_rest:
        delta_x += direction
        # print(f'Checking ({x + delta_x}, {y}).')
        if (x + delta_x, y) in clay:
            # we found a wall, return the last pos of water before the wall
            # print(f'Found wall at ({x + delta_x}, {y}).')
            return True, delta_x - direction
    # if we end up here, we found a drop
    # but we need to check if there is
    # print(f'Found drop at ({x + delta_x}, {y}).')
    return False, delta_x


# f_name = 'ex2.txt'
f_name = 'input.txt'

# spring of water is at
spring = (500, 0)

# data structures
clay = set()
water_at_rest = set()
moving_water = set()
water_flow_queue = []

with open(f_name, 'r') as f:
    # find x and y parts
    for line in f.readlines():
        x_part = re.search(r'x=([\d.]+)', line)
        y_part = re.search(r'y=([\d.]+)', line)
        x_vals = list(map(int, re.findall(r'(\d+)', x_part.group())))
        y_vals = list(map(int, re.findall(r'(\d+)', y_part.group())))
        # loop through all x values
        for x in range(min(x_vals), max(max(x_vals), min(x_vals)) + 1):
            for y in range(min(y_vals), max(max(y_vals), min(y_vals)) + 1):
                clay.add((x, y))


# pour water until we reach the bottom
bottom = False
# add first flowing water (one below the spring
water_flow_queue = [(500, 1)]
moving_water = {(500, 1)}
min_x, max_x, min_y, max_y = get_dims()
# print_map()

while not bottom:
    while water_flow_queue:
        next_water = water_flow_queue.pop(0)
        # print(f'Processing flowing water: {next_water}')
        # print_map()
        if next_water[1] > max_y:
            bottom = True
        else:
            pour_water(next_water[0], next_water[1], water_at_rest, moving_water, water_flow_queue)
    # water_flow_queue = sorted(moving_water, key=lambda x: (x[1], x[0]))


# now count the water at rest and moving water tiles that are within the boundaries
part1 = sum(1 for w in water_at_rest) + sum(1 for w in moving_water if min_y <= w[1] <= max_y)
print(f'Dims: min_x: {min_x}, max_x: {max_x}, min_y: {min_y}, max_y: {max_y}')
print(f'Total water at rest: {len(water_at_rest)}, total flowing water: {len(moving_water)}')
print(f'Part 1: {part1}')

# Dims: min_x: 460, max_x: 734, min_y: 6, max_y: 1679
# Total water at rest: 30551, total flowing water: 7822
# Part 1: 38364
# Part 2: 30551 (just the water at rest number!)
