# Load any required modules. Most commonly used:

import re

# from collections import defaultdict, deque

# from utils.aoctools import aoc_timer


class Node:
    """Element in a double linked list.
    Each node has a left and right neighbor."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self) -> str:
        return f"{self.value} l: {self.left.value} r: {self.right.value}"


class LinkedList:
    """Double linked list. Each node has left and right
    neighbors."""

    def __init__(self) -> None:
        self.start = None
        self.pointer = None
        self.length = 0

    def insert(self, node: Node):
        """Insert a new node after the pointer and start nodes."""
        if not self.start and not self.pointer:
            # empty list, create new start and pointer node
            self.start = node
            node.left = self.start
            node.right = self.start
            self.pointer = self.start
        else:
            # insert after pointer and before start
            node.left = self.pointer
            node.right = self.start
            self.start.left = node
            self.pointer.right = node
            self.pointer = node
        self.length += 1

    def shift_left(self):
        """Move pointer to the left by one step."""
        self.pointer = self.pointer.left

    def shift_right(self):
        """Move pointer to the right by one step."""
        self.pointer = self.pointer.right

    def move_node(self, node, n):
        """Move a provided node by n steps."""
        # determine move direction by sign of n
        # if 0 steps, just return and do nothing.
        if n == 0:
            return
        # else, determine move function
        if n < 0:
            f_move = self.shift_left
            # turn steps to a positive number and add 1 as
            # we insert BEFORE the pointer when moving negative direction
            steps = (-1 * n) + 1
        elif n > 0:
            f_move = self.shift_right
            steps = n

        self.pointer = node
        # move number of steps
        for _ in range(steps):
            f_move()
        # now repoint node and pointer
        node.right = self.pointer.right
        self.pointer.right.left = node
        self.pointer.left = node.left.right
        node.left.right = self.pointer
        self.pointer.right = node
        node.left = self.pointer

    def __repr__(self) -> str:
        return f"Start: {self.start}, pointer: {self.pointer}, nodes: {self.length}"


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # signed ints
    regex = re.compile(r"(-?\d+)")

    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            matches = regex.findall(line.strip())
            if matches:
                puzzle_input.append(list(map(int, matches)))

    return puzzle_input


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.
    What is the sum of the three numbers that form the grove coordinates? The
    grove coordinates can be found by looking at the 1000th, 2000th, and 3000th
    numbers after the value 0, wrapping around the list as necessary.
    """
    count_elements = len(puzzle_input)
    print(f"Input has {count_elements} elements.")
    ll = LinkedList()
    # keep a list of node elements
    nodes = dict()
    for i, n in enumerate(puzzle_input):
        node = Node(n)
        ll.insert(node)
        nodes[i] = node

    # print some test output:
    print("Nodes:")
    print(nodes)
    print("Linked List")
    print(ll)
    # move to the right twice and print list
    for i in nodes:
        node = nodes[i]
        ll.move_node(node, node.value)
        print(f"{node.value} moves.")
        print(ll)
    # to calculate the 1000th, 2000th number after 0,
    # - find 0 and its index
    # - take (1000 + index of 0) % <length of list>
    # - this is the index of the number we are looking for

    return 1


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/20.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start:  End:
# Part 2: Start:  End:
