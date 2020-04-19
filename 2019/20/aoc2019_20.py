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
    portals = defaultdict(list)
    logging.info('Finding portals.')

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

def get_neighbors(grid, portal_paths, current_pos):
    r, c = current_pos
    neighbors = [(r, c+1), (r, c-1), (r+1, c), (r-1, c)]
    valid_neighbors = []
    for n in neighbors:
        x = grid[n[0]][n[1]]
        if x == '.':
            valid_neighbors.append(n)
        elif n in portal_paths:
            valid_neighbors.append(portal_paths[n])
    
    return valid_neighbors


def find_portals(grid):
    portals = defaultdict(list)

    # find upper and lower dimensions of grid
    up_bound = 0
    left_bound = 0
    bot_bound = len(grid) - 1
    right_bound = len(grid[0]) - 1

    # find letters, then review all 4 neighbors
    for r, line in enumerate(grid):
        for c, x in enumerate(line):
            if x in ascii_uppercase:
                neighbors = [(r, c+1), (r, c-1), (r+1, c), (r-1, c)] 
                out_coord = (-1, -1)
                # check right neighbor for additional letter
                n_r, n_c = neighbors[0]
                b_r, b_c = neighbors[2]
                if grid[n_r][n_c] in ascii_uppercase:
                    first = x
                    second = grid[n_r][n_c]
                    # now the '.' is either to right or left
                    n_l_r, n_l_c = r, c - 1
                    n_r_r, n_r_c = r, n_c + 1
                    # to the left
                    if grid[n_l_r][n_l_c] == '.':
                        # out coordinate is n_l_r, n_l_c
                        out_coord = (n_l_r, n_l_c)
                        in_coord = (r, c)
                    # to the right
                    elif grid[n_r_r][n_r_c] == '.':
                        # out coordinate is n_r_r, n_r_c
                        out_coord = (n_r_r, n_r_c)
                        in_coord = (n_r, n_c)
                # check bottom neighbor for additional letter
                elif grid[b_r][b_c] in ascii_uppercase:
                    first = x
                    second = grid[b_r][b_c]
                    # now the '.' is either above or below
                    n_a_r, n_a_c = r - 1, c
                    n_b_r, n_b_c = b_r + 1, c
                    # above
                    if grid[n_a_r][n_a_c] == '.':
                        # out coordinate is n_a_r, n_a_c
                        out_coord = (n_a_r, n_a_c)
                        in_coord = (r, c)
                    # below
                    elif grid[n_b_r][n_b_c] == '.':
                        # out coordinate is n_b_r, n_b_c
                        out_coord = (n_b_r, n_b_c)
                        in_coord = (b_r, b_c)

                # if we found an out_coord, create a new portal
                if out_coord != (-1, -1):
                    name = f'{first}{second}'
                    portals[name].append(Portal(name, in_coord, out_coord))
                    logging.debug(f'Found portal {name} at {portals[name]}.')

    # generate dictionary of entry / exit paths (i.e. connecting ins and outs of each pair of portals)
    portal_paths = dict()
    for portal in portals:
        if portal not in ['AA', 'ZZ']:
            p1, p2 = portals[portal]
            portal_paths[p1.in_coord] = p2.out_coord
            portal_paths[p2.in_coord] = p1.out_coord

    return portals, portal_paths



#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    Portal = namedtuple('Portal', ['name', 'in_coord', 'out_coord'])

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
    aa = portals['AA'][0].out_coord
    zz = portals['ZZ'][0].out_coord

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
    
