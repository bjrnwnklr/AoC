# AOC 2019, day 18
import logging
from string import ascii_lowercase, ascii_uppercase
from collections import defaultdict, deque


# find all valid neighbors of a grid element
def neighbors(grid, coord):

    # west, north, east, south
    _neighbor_pos = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    neighbor_coords = [(coord[0] + n[0], coord[1] + n[1]) for n in _neighbor_pos]
    valid_neighbors = [n for n in neighbor_coords if grid[n] != '#']
    return valid_neighbors





#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    f_name = 'ex1.txt'


    grid = dict()
    keys = dict()
    doors = dict()
    door_pos = dict()

    f = open(f_name, 'r')
    for y, line in enumerate(f.readlines()):
        for x, c in enumerate(line.strip('\n')):
            grid[(x, y)] = c
            if c in ascii_lowercase:
                keys[c] = (x, y)
            elif c in ascii_uppercase:
                doors[c] = (x, y)
                door_pos[(x, y)] = c
            elif c == '@':
                start = (x, y)


    logging.debug('Keys found: {}'.format(keys))
    logging.debug('Doors found: {}'.format(doors))
    logging.debug('Door positions: {}'.format(door_pos))

    # run BFS from start (later repeat from each key - 
    # map out number of steps and doors between start (or key) and all other keys)
    player = start
        
    # BFS stuff
    # q contains the following:
    # 0: current position (x, y) tuple
    # 1: current path (length of steps)
    # 2: doors encountered (list)
    q = deque([(player, 0, [])])
    seen = set()
    # path stores the path to each individual point in the grid as explored by BFS
    path = defaultdict(list)
    doors_from = defaultdict(list)
    # key_graph stores the number of steps and doors between the start and the respective key
    key_graph = dict()

    # run BFS until we have explored every grid cell
    while(q):

        # removes element from the right side of the queue
        current_pos, current_path, current_doors = q.pop()

        # once at current_pos, find all valid neighbours
        for next_step in neighbors(grid, current_pos):
            if (next_step not in seen):

                seen.add(next_step)
                path[next_step] = current_path + 1

                # check if we found a door
                if next_step in door_pos:
                    updated_doors = current_doors + [door_pos[next_step]]
                else:
                    updated_doors = current_doors[:]
                doors_from[next_step] = updated_doors[:]

                q.appendleft((next_step, current_path + 1, updated_doors[:]))


    # BFS from start finished, print the steps / doors between start and the keys
    for k in keys:
        logging.debug('Steps and doors from start to {} ({}): {}, {}'.format(
            k, keys[k], path[keys[k]], doors_from[keys[k]]))
