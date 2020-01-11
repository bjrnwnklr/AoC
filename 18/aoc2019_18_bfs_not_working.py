# AOC 2019, day 18
import logging
from string import ascii_lowercase, ascii_uppercase
from collections import defaultdict, deque


def test_bit(bit_baseline, bit_to_test):
    return (bit_baseline & bit_to_test) == bit_baseline

def set_bit(bit_baseline, bit_to_set):
    return bit_baseline | bit_to_set

# find all valid neighbors of a grid element
def neighbors(grid, coord):

    # west, north, east, south
    _neighbor_pos = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    neighbor_coords = [(coord[0] + n[0], coord[1] + n[1]) for n in _neighbor_pos]
    valid_neighbors = [n for n in neighbor_coords if grid[n] != '#']
    return valid_neighbors

# find all valid neighbors of a grid element
def reachable_keys(key_graph, current_pos):

    key, key_mask = current_pos
    # logging.debug('Looking for neighbors for key {} with mask {:026b}'.format(key, key_mask))
    # valid_neighbors = [(k, key_mask) for k, _, target_mask in key_graph[key] if test_bit(target_mask, key_mask)]
    valid_neighbors = []
    for k, _, target_mask in key_graph[key]:
        # logging.debug('Potential neighbor: {}, {:0b}'.format(k, target_mask))
        if test_bit(target_mask, key_mask):
            valid_neighbors.append((k, key_mask))
            # logging.debug('({}, {:0b}) is a valid neighbor'.format(k, target_mask))
    # logging.debug('Valid neighbors for key {} are: {}'.format(key, valid_neighbors))
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


#### Global variables
# dictionary with bit set per key in alphabetical order (e.g. for 'a', 1st bit is set, for 'z' 26th bit is set)
key_bits = {x: 1 << i for i, x in enumerate(ascii_lowercase)}
door_bits = {x: 1 << i for i, x in enumerate(ascii_uppercase)}
# "No key" bit mask - bit 26 is set
start_key_mask = 1 << 26


#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    f_name = 'ex2.txt'

    # main grid, used for the first BFS to generate map of keys
    grid = dict()
    # position of keys (e.g. keys[(x, y)] = 'a')
    keys = dict()
    # position of doors (e.g. doors[(x, y)] = 'A')
    doors = dict()
    

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

    # list of key positions - we will iterate over this
    key_positions = {v: k for k, v in keys.items()}

    # success criteria - what does the bitmask look like when we have all the keys?
    full_keys = start_key_mask
    for k in key_positions:
        full_keys = set_bit(full_keys, key_bits[k])

    logging.debug('Full keys bitmask: {} ({:026b})'.format(full_keys, full_keys))

    # run BFS from start first and map out paths to each key from start.
    # We will then iterate over all key positions, but ignore the start position (we don't need an edge from key to start, only from start to key)
    path, keys_found, doors_from = map_keys_BFS(grid, start, doors, keys)
    for other_key in keys_found:
        key_graph['@'].add((other_key, path[key_positions[other_key]], doors_from[key_positions[other_key]]))
    for key in key_positions:
        path, keys_found, doors_from = map_keys_BFS(grid, key_positions[key], doors, keys)
        # update graph_dict with edges between keys
        # edge is a set of (key, steps, bit encoded doors between) tuples
        # e.g. graph_dict['a'] = {('f', 44, 0b101)}
        for other_key in keys_found:
            if other_key != key:
                key_graph[key].add((other_key, path[key_positions[other_key]], doors_from[key_positions[other_key]]))
                key_graph[other_key].add((key, path[key_positions[other_key]], doors_from[key_positions[other_key]]))


    # BFS from start finished, print the steps / doors between start and the keys
    # for k in key_graph:
        # logging.debug('Steps and doors from start to {} ({}): {}, {:026b}'.format(
            # k, keys[k], path[k], doors_from[k]))
        # logging.debug('Key graph for {}: {}'.format(k, key_graph[k]))

    # now run another BFS on the key_graph, starting from start position.
    # BFS stuff
    # q contains the following:
    # 0: current position (key, key bitmap) tuple
    # 1: current path (list of keys)
    # 2: length of steps
    keywalk_start = ('@', start_key_mask)
    q = deque([(keywalk_start, (), 0)])
    seen = set()
    distance_to = defaultdict(lambda: 1e09)
    endstates = []


    while(q):

        # removes element from the right side of the queue
        current_pos, current_path, current_steps = q.pop()

        if current_pos in seen:
            continue
    
        seen.add(current_pos)
        current_path += (current_pos, )

        # check if we found a key (we should since the nodes are all keys)
        # update the keys we hold...
        if current_pos[0] in key_positions:
            new_keys = set_bit(current_pos[1], key_bits[current_pos[0]])
            current_pos = (current_pos[0], new_keys)

        # check if we reached the end
        if current_pos[1] == full_keys:
            endstates.append((current_steps, current_path))
            break

        for next_step in reachable_keys(key_graph, current_pos):
            # get number of steps to next_step 
            add_steps = [s for k, s, _ in key_graph[current_pos[0]] if k == next_step[0]][0]
            q.appendleft(((next_step[0], current_pos[1]), current_path, current_steps + add_steps))

    """        
    # run BFS until we have explored every edge in the graph
    while(q):

        # removes element from the right side of the queue
        current_pos, current_path, current_steps = q.pop()

        # check if we reached the end
        if current_pos[1] == full_keys:
            # logging.debug('Found end state at {}'.format(current_pos))
            # logging.debug('Current path: {}'.format(current_path))
            # logging.debug('Number of steps: {}'.format(current_steps))
            endstates.append((current_pos, current_path, current_steps))
            continue

        # once at current_pos, find all valid neighbours
        for next_step in reachable_keys(key_graph, current_pos):
            if (next_step not in seen):

                seen.add(next_step)
                path[next_step] = current_path + [next_step]

                # get number of steps
                add_steps = [s for k, s, _ in key_graph[current_pos[0]] if k == next_step[0]][0]


                # check if we found a key and modify the key_mask
                if next_step[0] in key_positions:
                    key_mask = set_bit(next_step[1], key_bits[next_step[0]])
                    # logging.debug('Picked up key {} and updated bitmask to {}'.format(next_step[0], key_mask))
                else:
                    key_mask = next_step[1]
                
                ## -->> THIS is very likely incorrect - should be steps[(next_step[0], key_mask)]
                if current_steps + add_steps < steps[next_step]:
                    steps[next_step] = current_steps + add_steps
                    # logging.debug('Adding key ({}, {}) to queue.'.format(next_step[0], key_mask))
                    q.appendleft(((next_step[0], key_mask), current_path + [next_step], current_steps + add_steps))
    """

    # BFS finished
    logging.debug('Graph traversal BFS finished.')

    # logging.info('Endstates found at: {}'.format(endstates))
    # shortest_steps, shortest_path = min(endstates, key=lambda x: x[0])
    # logging.info('Shortest number of steps is {} with the path {}.'.format(shortest_steps, shortest_path))

    for e in endstates:
        print('Endstate: {}'.format(e[0]))