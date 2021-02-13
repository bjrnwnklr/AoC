import re


class Node:
    def __init__(self, df):
        nums = list(map(int, re.findall(r'\d+', df)))
        self.x, self.y, self.size, self.used, self.avail = nums[0:5]
        self.coords = (self.x, self.y)

    def __repr__(self):
        return f'Node ({self.x}, {self.y}): {self.size} / {self.used} / {self.avail}'

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


if __name__ == '__main__':
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
