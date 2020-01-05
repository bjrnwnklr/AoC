# AOC 2019, day 18
import logging
from string import ascii_lowercase, ascii_uppercase
from collections import defaultdict, deque, namedtuple


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

#### Global variables
# dictionary with bit set per key in alphabetical order (e.g. for 'a', 1st bit is set, for 'z' 26th bit is set)
key_bits = {x: 1 << i for i, x in enumerate(ascii_lowercase)}
door_bits = {x: 1 << i for i, x in enumerate(ascii_uppercase)}
# "No key" bit mask - bit 26 is set
start_key_mask = 1 << 26


#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    f_name = 'input.txt'

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

    logging.info('Keys found: {}'.format(keys))
    logging.info('Doors found: {}'.format(doors))

    # list of key positions - we will iterate over this
    key_positions = {v: k for k, v in keys.items()}

    # success criteria - what does the bitmask look like when we have all the keys?
    full_keys = start_key_mask
    for k in key_positions:
        full_keys = set_bit(full_keys, key_bits[k])

    logging.debug('Full keys bitmask: {} ({:026b})'.format(full_keys, full_keys))

    
    # now run another BFS on the key_graph, starting from start position.
    # BFS stuff
    # q contains the following:
    # 0: current position (key, key bitmap) tuple
    # 1: current path (list of steps)
    # 2: keys found (list of keys found along the way)
    # 2: length of steps
    Point = namedtuple('Point', ['pos', 'key_mask'])
    keywalk_start = Point(start, start_key_mask)
    q = deque([(keywalk_start, 0)])
    seen = set()
    # path stores the path to each individual point in the grid as explored by BFS
    # path = defaultdict(list)
    endstates = []

    # run BFS until we have explored every edge in the graph
    while(q):

        # removes element from the right side of the queue
        # current_point, current_keys, current_steps = q.pop()
        current_point, current_steps = q.pop()

        if current_point not in seen:
            seen.add(current_point)

            if len(seen) % 10000 == 0:
                logging.info('Seen: {}'.format(len(seen)))

            # check if we come to a door and we don't have the key - skip to next loop
            if current_point.pos in doors and not test_bit(door_bits[doors[current_point.pos]], current_point.key_mask):
                continue

            new_key_mask = current_point.key_mask
            # new_keys_found = current_keys[:]
            # check if we come to a key and pick it up
            if current_point.pos in keys:
                logging.debug('Picked up key {} at {}.'.format(keys[current_point.pos], current_point.pos))
                new_key_mask = set_bit(new_key_mask, key_bits[keys[current_point.pos]])
                # new_keys_found.append(keys[current_point.pos])

                # check if we reached the end
                if new_key_mask == full_keys:
                    logging.info('Found end state at {}'.format(current_point.pos))
                    # logging.info('Keys found: {}'.format(new_keys_found))
                    logging.info('Number of steps: {}'.format(current_steps))
                    # endstates.append((current_point, new_keys_found, current_steps))
                    endstates.append((current_point, current_steps))
                    break

            # once at current_pos, find all valid neighbours
            for next_step in neighbors(grid, current_point.pos):
                next_point = Point(next_step, new_key_mask)

                # path[next_point] = current_path + [next_point]

                logging.debug('Adding key {} to queue.'.format(next_point))
                # q.appendleft((next_point, new_keys_found, current_steps + 1))
                q.appendleft((next_point, current_steps + 1))

    # BFS finished
    logging.debug('Graph traversal BFS finished.')

    logging.debug('Endstates found at: {}'.format(endstates))
    # shortest_pos, shortest_keys_found, shortest_steps = min(endstates, key=lambda x: x[2])
    shortest_pos, shortest_steps = min(endstates, key=lambda x: x[1])
    # logging.info('Shortest number of steps is {} with the path {}.'.format(shortest_steps, shortest_keys_found))
    logging.info('Shortest number of steps is {}.'.format(shortest_steps))
