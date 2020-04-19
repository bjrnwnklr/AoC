# AOC 2019, day 20
import logging
from string import ascii_uppercase
from collections import defaultdict, deque, namedtuple


def print_grid(grid, curr_pos = (0, 0)):
    for r, line in enumerate(grid):
        print(''.join('@' if (r, c) == curr_pos else x for c, x in enumerate(line)))

def parse_grid(grid):
        
    # find inner part of maze
    # find the middle of the grid and then search left, right, up and down until we find either . or #

    half_hor = len(grid[0]) // 2
    half_ver = len(grid) // 2
    logging.info(f'Searching for inner borders, starting at [{half_ver}, {half_hor}].')
    grid_chars = ['#', '.']

    in_top = in_bot = in_left = in_right = 0
    # search up
    curr_r = half_ver
    while in_top == 0:
        if grid[curr_r][half_hor] in grid_chars:
            in_top = curr_r + 1
            logging.debug(f'found inner top border at {in_top}.')
        else:
            curr_r -= 1

    curr_r = half_ver
    while in_bot == 0:
        if grid[curr_r][half_hor] in grid_chars:
            in_bot = curr_r - 1
            logging.debug(f'found inner bottom border at {in_bot}.')
        else: 
            curr_r += 1

    curr_c = half_hor
    while in_left == 0:
        if grid[half_ver][curr_c] in grid_chars:
            in_left = curr_c + 1
            logging.debug(f'found inner left border at {in_left}.')
        else:
            curr_c -= 1

    curr_c = half_hor
    while in_right == 0:
        if grid[half_ver][curr_c] in grid_chars:
            in_right = curr_c - 1
            logging.debug(f'found inner right border at {in_right}.')
        else:
            curr_c += 1

    # find portals in top line and in in_bot line (look for two letters underneath)
    # coordinates stored are 
    # - in: position of 2nd letter i.e. where you enter the portal
    # - out: position of dot i.e. where you exit the portal
    # - side: 0 if outer side, 1 if inner side
    portals = defaultdict(list)
    logging.info('Finding portals.')

    # top and in_bottom
    rows = [0, in_bot - 1]
    for i, r in enumerate(rows):
        for c, x in enumerate(grid[r]):
            next_r, next_c = r + 1, c 
            if x in ascii_uppercase and grid[next_r][next_c] in ascii_uppercase:
                name = f'{x}{grid[next_r][next_c]}'
                # check if this is inner or outer side
                side = 0 if i == 0 else 1
                portals[name].append(Portal(name, (next_r, c), (next_r + 1, c), side))
                logging.debug(f'Found portal {name} at {portals[name]}.')

    # in_top and bottom
    rows = [in_top, len(grid) - 2]
    for i, r in enumerate(rows):
        for c, x in enumerate(grid[r]):
            next_r, next_c = r + 1, c 
            if x in ascii_uppercase and grid[next_r][next_c] in ascii_uppercase:
                name = f'{x}{grid[next_r][next_c]}'
                # check if this is inner or outer side
                side = 1 if i == 0 else 0
                portals[name].append(Portal(name, (r, c), (r - 1, c), side))
                logging.debug(f'Found portal {name} at {portals[name]}.')

    # left and in_right
    cols = [0, in_right - 1]
    for r, line in enumerate(grid):
        for i, c in enumerate(cols):
            x = line[c]
            next_r, next_c = r, c + 1 
            if x in ascii_uppercase and grid[next_r][next_c] in ascii_uppercase:
                name = f'{x}{grid[next_r][next_c]}'
                # check if this is inner or outer side
                side = 0 if i == 0 else 1
                portals[name].append(Portal(name, (r, next_c), (r, next_c + 1), side))
                logging.debug(f'Found portal {name} at {portals[name]}.')

    # in_left and right
    cols = [in_left, len(grid[0]) - 2]
    for r, line in enumerate(grid):
        for i, c in enumerate(cols):
            x = line[c]
            next_r, next_c = r, c + 1 
            if x in ascii_uppercase and grid[next_r][next_c] in ascii_uppercase:
                name = f'{x}{grid[next_r][next_c]}'
                # check if this is inner or outer side
                side = 1 if i == 0 else 0
                portals[name].append(Portal(name, (r, c), (r, c - 1), side))
                logging.debug(f'Found portal {name} at {portals[name]}.')


    # generate dictionary of entry / exit paths (i.e. connecting ins and outs of each pair of portals)
    # if we go from inner portal to outer portal, go one level down
    # if we go from outer portal to inner portal, go one level up
    portal_paths = dict()
    for portal in portals:
        if portal not in ['AA', 'ZZ']:
            p1, p2 = portals[portal]
            # go one level down if p1.side is inner (==1)
            level = 1 if p1.side == 1 else -1
            portal_paths[p1.in_coord] = (*p2.out_coord, level)
            portal_paths[p2.in_coord] = (*p1.out_coord, -level)

    return portals, portal_paths

def get_neighbors(grid, portal_paths, current_pos):
    r, c , l = current_pos
    neighbors = [(r, c+1, l), (r, c-1, l), (r+1, c, l), (r-1, c, l)]
    valid_neighbors = []
    for n in neighbors:
        x = grid[n[0]][n[1]]
        if x == '.':
            valid_neighbors.append(n)
        elif (n[0], n[1]) in portal_paths:
            # check if we go one level up or down
            new_r, new_c, add_l = portal_paths[(n[0], n[1])]
            new_l = n[2] + add_l
            # if we are on level 0, ignore any outer portals
            if new_l >= 0:
                valid_neighbors.append((new_r, new_c, new_l))
    
    return valid_neighbors



#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    Portal = namedtuple('Portal', ['name', 'in_coord', 'out_coord', 'side'])

    f_name = 'input.txt'

    logging.info('Reading in grid.')

    # parse grid and fill the following variables:
    # - grid
    f = open(f_name, 'r')
    grid = []
    letters = dict()
    for y, line in enumerate(f.readlines()):
        grid_line = []
        for x, c in enumerate(line.strip('\n')):
            # add character into grid
            grid_line.append(c)            
        grid.append(grid_line)
    f.close()

    start = (0, 0)
    logging.debug(f'printing grid with start at ({start}).')
    print_grid(grid, start)


    portals, portal_paths = parse_grid(grid)
    # portals, portal_paths = find_portals(grid)

    # list all found portals
    logging.info(f'Found {len(portals)} portals.')
    for portal in sorted(portals):
        logging.debug(f'{portal}: {portals[portal]}')

    # list all paths
    logging.info(f'Found {len(portal_paths)} paths.')
    for p in portal_paths:
        logging.debug(f'{p} -> {portal_paths[p]}')


    # traverse grid using BFS, starting from AA and finding ZZ
    aa = (*portals['AA'][0].out_coord, 0)
    zz = (*portals['ZZ'][0].out_coord, 0)

    logging.info(f'Looking for shortest path from {aa} to {zz}.')


    # queue = position, number of steps
    q = deque([(aa, 0)])
    seen = set()

    while(q):
        current_pos, current_steps = q.pop()

        if current_pos in seen:
            continue

        seen.add(current_pos)

        if current_pos == zz:
            logging.info(f'Found ZZ, steps: {current_steps}')
            break

        # go through neighbors using the graph
        for neighbor in get_neighbors(grid, portal_paths, current_pos):
            if neighbor not in seen:
                logging.debug(f'Pushing {neighbor}, {current_steps + 1} into queue')
                q.appendleft((neighbor, current_steps + 1))

    logging.info('BFS ended!')

    # Part 1 answer: 400
    # Part 2 answer: 4986
