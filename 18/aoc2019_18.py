# AOC 2019, day 18
import logging
from string import ascii_lowercase, ascii_uppercase
from collections import defaultdict, deque


def test_bit(bit_baseline, bit_to_test):
    return bit_baseline & bit_to_test

def set_bit(bit_baseline, bit_to_set):
    return bit_baseline | bit_to_set

# find all valid neighbors of a grid element
def neighbors(grid, coord):

    # west, north, east, south
    _neighbor_pos = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    neighbor_coords = [(coord[0] + n[0], coord[1] + n[1]) for n in _neighbor_pos]
    valid_neighbors = [n for n in neighbor_coords if grid[n] != '#']
    return valid_neighbors


def map_keys_BFS(grid, start, doors):
    # BFS stuff
    # q contains the following:
    # 0: current position (x, y) tuple
    # 1: current path (length of steps)
    # 2: doors encountered (list)
    q = deque([(start, 0, 0)])
    seen = set()
    # path stores the path to each individual point in the grid as explored by BFS
    path = defaultdict(list)
    # stores a bitcoded register of doors between start and current position (bit set per door on path)
    doors_from = defaultdict(int)

    # run BFS until we have explored every grid cell
    while(q):

        # removes element from the right side of the queue
        current_pos, current_path, current_doors = q.pop()

        # once at current_pos, find all valid neighbours
        for next_step in neighbors(grid, current_pos):
            if (next_step not in seen):

                seen.add(next_step)
                path[next_step] = current_path + 1

                # check if we found a door and add it to list of doors between start and next_step
                if next_step in doors:
                    current_doors = set_bit(current_doors, door_bits[doors[next_step]])
                doors_from[next_step] = current_doors

                q.appendleft((next_step, current_path + 1, current_doors))

    return path, doors_from


#### Global variables
# dictionary with bit set per key in alphabetical order (e.g. for 'a', 1st bit is set, for 'z' 26th bit is set)
key_bits = {x: 1 << i for i, x in enumerate(ascii_lowercase)}
door_bits = {x: 1 << i for i, x in enumerate(ascii_uppercase)}
full_keys = (1 << 26) - 1


#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    f_name = 'ex2.txt'

    # main grid, used for the first BFS to generate map of keys
    grid = dict()
    # position of keys (e.g. keys['a'] = (x, y))
    keys = dict()
    # position of doors (e.g. doors['A'] = (x, y))
    doors = dict()
    # doors per position (e.g. door_pos[(x, y)] = 'A')
    door_pos = dict()


    # parse grid and fill the following variables:
    # - grid
    # - keys
    # - doors
    # - door_pos
    # - start
    f = open(f_name, 'r')
    for y, line in enumerate(f.readlines()):
        for x, c in enumerate(line.strip('\n')):
            grid[(x, y)] = c
            if c in ascii_lowercase:
                keys[(x, y)] = c
            elif c in ascii_uppercase:
                doors[(x, y)] = c
            elif c == '@':
                start = (x, y)
    f.close()

    logging.debug('Keys found: {}'.format(keys))
    logging.debug('Doors found: {}'.format(doors))

    # key_graph stores the number of steps and doors between the start and the respective key
    key_graph = defaultdict(set)

    # run BFS from start (later repeat from each key - 
    # map out number of steps and doors between start (or key) and all other keys)
    
    for player in [start] + list(keys.keys()):
        logging.debug('Parsing grid from {}'.format(grid[player]))
        path, doors_from = map_keys_BFS(grid, player, doors)
        # update graph_dict with edges between keys
        # edge is a set of (key, steps, bit encoded doors between) tuples
        # e.g. graph_dict['a'] = {('f', 44, 0b101)}
        for k in keys:
            key_graph[player].add((k, path[k], doors_from[k]))
            key_graph[k].add((player, path[k], doors_from[k]))


    # BFS from start finished, print the steps / doors between start and the keys
    for k in key_graph:
        # logging.debug('Steps and doors from start to {} ({}): {}, {:026b}'.format(
            # k, keys[k], path[k], doors_from[k]))
        logging.debug('Graph dict for {}: {}'.format(k, key_graph[k]))
