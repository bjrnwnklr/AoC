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
    logging.debug(f'Searching for inner borders, starting at [{half_ver}, {half_hor}].')
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
    portals = defaultdict(list)
    logging.debug('Finding portals.')

    # top and in_bottom
    rows = [0, in_bot - 1]
    for r in rows:
        for c, x in enumerate(grid[r]):
            next_r, next_c = r + 1, c 
            if x in ascii_uppercase and grid[next_r][next_c] in ascii_uppercase:
                name = f'{x}{grid[next_r][next_c]}'
                portals[name].append(Portal(name, (next_r, c), (next_r + 1, c)))
                logging.debug(f'Found portal {name} at {portals[name]}.')

    # in_top and bottom
    rows = [in_top, len(grid) - 2]
    for r in rows:
        for c, x in enumerate(grid[r]):
            next_r, next_c = r + 1, c 
            if x in ascii_uppercase and grid[next_r][next_c] in ascii_uppercase:
                name = f'{x}{grid[next_r][next_c]}'
                portals[name].append(Portal(name, (r, c), (r - 1, c)))
                logging.debug(f'Found portal {name} at {portals[name]}.')

    # left and in_right
    cols = [0, in_right - 1]
    for r, line in enumerate(grid):
        for c in cols:
            x = line[c]
            next_r, next_c = r, c + 1 
            if x in ascii_uppercase and grid[next_r][next_c] in ascii_uppercase:
                name = f'{x}{grid[next_r][next_c]}'
                portals[name].append(Portal(name, (r, next_c), (r, next_c + 1)))
                logging.debug(f'Found portal {name} at {portals[name]}.')

    # in_left and right
    cols = [in_left, len(grid[0]) - 2]
    for r, line in enumerate(grid):
        for c in cols:
            x = line[c]
            next_r, next_c = r, c + 1 
            if x in ascii_uppercase and grid[next_r][next_c] in ascii_uppercase:
                name = f'{x}{grid[next_r][next_c]}'
                portals[name].append(Portal(name, (r, c), (r, c - 1)))
                logging.debug(f'Found portal {name} at {portals[name]}.')


    # generate dictionary of entry / exit paths (i.e. connecting ins and outs of each pair of portals)
    portal_paths = dict()
    for portal in portals:
        if portal not in ['AA', 'ZZ']:
            p1, p2 = portals[portal]
            portal_paths[p1.in_coord] = p2.out_coord
            portal_paths[p2.in_coord] = p1.out_coord

    return portals, portal_paths

def get_neighbors(grid, portal_paths, r, c):
    neighbors = [(r, c+1), (r, c-1), (r+1, c), (r-1, c)]
    valid_neighbors = []
    for n in neighbors:
        x = grid[n[0]][n[1]]
        if x == '.':
            valid_neighbors.append(n)
        elif x in portal_paths:
            valid_neighbors.append(portal_paths[x])
    
    return valid_neighbors


def map_keys_BFS(grid, start, doors, keys):
    # BFS stuff
    # q contains the following:
    # 0: current position (x, y) tuple
    # 1: current path (length of steps)
    # 2: doors encountered (bitmask)
    q = deque([(start, 0, start_key_mask)])
    seen = set()
    # path stores the path to each individual point in the grid as explored by BFS
    path = defaultdict(int)
    # stores a bitcoded register of doors between start and current position (bit set per door on path)
    doors_from = defaultdict(int)
    # keys found neighboring "start" (only real next neighbors)
    keys_found = set()

    # run BFS until we have explored every grid cell
    while(q):

        # removes element from the right side of the queue
        current_pos, current_path, current_doors = q.pop()

        if current_pos in seen:
            continue

        seen.add(current_pos)
        path[current_pos] = current_path

        new_doors = current_doors
        if current_pos in doors:
            new_doors = set_bit(current_doors, door_bits[doors[current_pos]])
        doors_from[current_pos] = new_doors

        if current_pos in keys:
            keys_found.add(keys[current_pos])

        # once at current_pos, find all valid neighbours
        for next_step in neighbors(grid, current_pos):
            q.appendleft((next_step, current_path + 1, new_doors))

    return path, keys_found, doors_from

#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    Portal = namedtuple('Portal', ['name', 'in_coord', 'out_coord'])

    f_name = 'example1.txt'

    logging.debug('reading in grid.')

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

    # list all found portals
    logging.debug(f'Found {len(portals)} portals.')
    for portal in sorted(portals):
        logging.debug(f'{portal}: {portals[portal]}')

    # list all paths
    logging.debug(f'Found {len(portal_paths)} paths.')
    for p in portal_paths:
        logging.debug(f'{p} -> {portal_paths[p]}')


    # traverse grid using BFS, starting from AA and finding ZZ

