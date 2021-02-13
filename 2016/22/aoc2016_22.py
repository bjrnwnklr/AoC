import re
from collections import deque

class Node:
    def __init__(self, df):
        nums = list(map(int, re.findall(r'\d+', df)))
        self.x, self.y, self.size, self.used, self.avail = nums[0:5]
        self.coords = (self.x, self.y)

    def __repr__(self):
        return f'Node ({self.x}, {self.y}): {self.size} / {self.used} / {self.avail}'

    def __str__(self):
        return f'{self.used:3}/{self.size:3}'

    def __eq__(self, other_node):
        return self.coords == other_node.coords

    def is_empty(self):
        return self.used == 0

    def fits_on(self, other_node):
        return self != other_node and self.used <= other_node.avail


class Cluster:
    def __init__(self):
        self.grid = dict()
        self.viable_pairs = set()

    def __repr__(self):
        return f'Cluster - {len(self.grid)} nodes'

    def print_grid(self):
        for y in range(max(n[1] for n in self.grid) + 1):
            print(' -- '.join(str(self.grid[(x, y)]) for x in range(max(n[0] for n in self.grid) + 1)))

    def add_node(self, node):
        self.grid[(node.x, node.y)] = node

    def calc_viable_pairs(self):
        """
        Calculate a set of viable pairs.
        """
        for node_a in [a for a in self.grid.values() if not a.is_empty()]:
            # set.update() used here as we use a generator expression to calculate a set of
            # viable pairs. if we use set.add(), we would add a generator object to the
            # set.
            self.viable_pairs.update((node_a.coords, node_b.coords)
                                     for node_b in self.grid.values() if node_a.fits_on(node_b))

    def viable_pairs_count(self):
        return len(self.viable_pairs)

    def bfs(self, start, target):
        n_coords = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        q = deque([(start, 0)])
        seen = set()
        while q:
            curr_node, curr_steps = q.popleft()

            # found the target, return number of steps required
            if curr_node == target:
                return curr_steps

            if curr_node not in seen:
                seen.add(curr_node)
                # check all neighbors
                for n in [(curr_node[0] + dn[0], curr_node[1] + dn[1]) for dn in n_coords]:
                    if n in self.grid and self.grid[n].used <= self.grid[curr_node].size:
                        q.append((n, curr_steps + 1))

        # no path found
        return -1


if __name__ == '__main__':
    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    cluster = Cluster()
    with open(f_name, 'r') as f:
        disk_usage = f.readlines()[2:]
        for line in disk_usage:
            cluster.add_node(Node(line.strip()))

    print(cluster)

    cluster.calc_viable_pairs()
    print(f'Number of viable pairs: {cluster.viable_pairs_count()}')

    # part 1: 934

    # Part 2 ---

    # cluster.print_grid()

    # We can probably manually count the required steps:
    # 1) count how many steps the empty node takes to get to the left of the top right node
    # 2) each move of the data (starting from top right) to one node to the left takes 5 steps
    # 3) plus one final step for the last grid

    # we can either count 1) on the grid manually (we seem to have to move around a wall in the middle),
    # or do a BFS
    # Steps:
    # 11 up
    # 9 left
    # 16 up
    # 25 right
    # 29 * 5 hops left
    # 1 final step
    # = 207 steps, which is correct!

    # part 2: 207

    # let's solve it programmatically
    steps = 0
    # the x coordinate of the node 1 left of the top right corner, 29 for the 30x30 grid in the puzzle
    target_x = max(n[0] for n in cluster.grid) - 1
    # find the node with the 0 used disk, (13, 27) in the puzzle
    movable_node = [n.coords for n in cluster.grid.values() if n.used == 0][0]
    print(f'Movable node is at {movable_node}')

    # BFS find the shortest path to the top right (29, 0) node
    target_node = (target_x, 0)
    steps += cluster.bfs(movable_node, target_node)

    # calculate the number of hops required (29 * 5 + 1)
    steps += target_x * 5 + 1

    print(f'Part 2: {steps}')
