# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
# from utils.aoctools import aoc_timer


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

    # Extract ints from the input
    #
    # signed ints
    # regex = re.compile(r"(-?\d+)")
    #
    # unsigned ints
    # regex = re.compile(r"(\d+)")
    #
    # with open(f_name, "r") as f:
    #     puzzle_input = []
    #     for line in f.readlines():
    #         matches = regex.findall(line.strip())
    #         if matches:
    #             puzzle_input.append(list(map(int, matches)))

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

def add_up(node: Node, threshold: int = 100_000) -> int:
    """Sums up the total sizes of each node if <= threshold, recursively"""
    
    inc = node.total_size if node.total_size <= threshold else 0
    print(f'Adding {node.name} size: {node.total_size}, inc: {inc}')
    return inc + sum(add_up(n) for n in node.children.values())


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.
    
    Find all directories with size <= 100_000; what is
    the sum of the total sizes of those directories?

    Directories contained in other directories count
    multiple times.
    """
    # store Node elements for each directory
    dir_tree = {}
    # create root node and store in tree
    curr_node = Node('/', None)
    dir_tree['/'] = curr_node

    for line in puzzle_input:
        match line.split():
            case ['$', 'cd', d] if d == '..':
                # go up one directory
                curr_node = curr_node.parent
                print(f'Going up one dir. Current node: {curr_node.name}')
            case ['$', 'cd', d]:
                # add dir to curr_dir list
                curr_node = dir_tree[d]
                print(f'Changing to dir {d}. Current node: {curr_node.name}')
            case ['$', 'ls']:
                # we don't need to do anything, wait for file name
                pass
            case ['dir', d]:
                # found a directory, create a new node with current node as parent
                # check that we do not try to create a dir that already exists
                assert d not in dir_tree
                
                # add to children of current node
                new_dir = Node(d, curr_node)
                curr_node.children[d] = new_dir
                dir_tree[d] = new_dir
                print(f'New directory {d}. Current node: {curr_node.name}')
            case [size, name]:
                # found a file with size and name
                curr_node.inc_size(int(size))
                print(f'File {name} found with size {size}. Current node: {curr_node.name}')

    # find all directories with total_size <= 100_000
    print(dir_tree['/'])
    result = add_up(dir_tree['/'])
    print(f'Result: {result}')

    return result


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/07.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 14:23 End:
# Part 2: Start:  End:
