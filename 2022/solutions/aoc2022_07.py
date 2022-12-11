# Load any required modules. Most commonly used:

from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input

class Node:
    def __init__(self, name, parent) -> None:
        self.name = name
        self.parent = parent
        self.children = {}
        self.size = 0
        self.total_size = 0

    def __repr__(self) -> str:
        return f'[{self.name} p: {self.parent} s: {self.size} ts: {self.total_size} c: {self.children}]'

    def inc_size(self, s):
        """Add s to size and all parent directories"""
        self.total_size += s
        if self.parent:
            self.parent.inc_size(s)

def create_dir_tree(puzzle_input):
    """Parse the puzzle input and create a directory tree"""
        # create root node and store in tree
    curr_node = Node('/', None)
    root = curr_node

    for line in puzzle_input:
        match line.split():
            case ['$', 'cd', '/']:
                # go to root node
                curr_node = root
            case ['$', 'cd', '..']:
                # go up one directory
                curr_node = curr_node.parent
            case ['$', 'cd', d]:
                # change to child directory
                assert d in curr_node.children

                curr_node = curr_node.children[d]
            case ['$', 'ls']:
                # we don't need to do anything, wait for file name
                pass
            case ['dir', d]:
                # found a directory, create a new node with current node as parent
                assert d not in curr_node.children

                # add to children of current node
                curr_node.children[d] = Node(d, curr_node)
            case [size, _]:
                # found a file with size and name
                curr_node.inc_size(int(size))

    return root

def add_up(node: Node, threshold: int = 100_000) -> int:
    """Sums up the total sizes of each node if <= threshold, recursively"""
    
    inc = node.total_size if node.total_size <= threshold else 0
    return inc + sum(add_up(n) for n in node.children.values())

def find_space(node: Node, size: int, dirs: list) -> int:
    """Find all directories in the node structure that 
    frees up space of size, recursively."""
    if node.total_size >= size:
        dirs.append(node.total_size)
    for c in node.children.values():
        find_space(c, size, dirs)


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.
    
    Find all directories with size <= 100_000; what is
    the sum of the total sizes of those directories?

    Directories contained in other directories count
    multiple times.
    """

    # create the tree structure
    root = create_dir_tree(puzzle_input)
    # find all directories with total_size <= 100_000
    result = add_up(root)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value.
    
    Find the smallest directory that, if deleted, would free up enough space 
    on the filesystem to run the update. What is the total size of that directory?

    Total disk space 70_000_000
    Need unused space 30_000_000
    """
    # create the tree structure
    root = create_dir_tree(puzzle_input)

    # find how much space is required
    total_disk = 70_000_000
    required_space = 30_000_000
    unused_space = total_disk - root.total_size
    to_delete_space = required_space - unused_space
    if to_delete_space > 0:
        dirs = []
        find_space(root, to_delete_space, dirs)

    return min(dirs)


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/07.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 14:23 End: 15:45
# Part 2: Start: 15:46 End: 16:09

# Elapsed time to run part1: 0.00090 seconds.
# Part 1: 1989474
# Elapsed time to run part2: 0.00084 seconds.
# Part 2: 1111607