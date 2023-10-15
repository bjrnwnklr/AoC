# Load any required modules. Most commonly used:

import re

# from collections import defaultdict, deque

from utils.aoctools import aoc_timer


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
                puzzle_input.append(list(map(int, matches))[0])

    return puzzle_input


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
        """Insert a new node after the current pointer."""

        if not self.start and not self.pointer:
            # empty list, create new start and pointer node
            self.start = node
            node.left = self.start
            node.right = self.start
            self.pointer = self.start
        else:
            # insert between pointer (left) and pointer's right (right)
            new_right = self.pointer.right
            # link pointer and node
            self.pointer.right = node
            node.left = self.pointer
            # link new right and node
            node.right = new_right
            new_right.left = node
            # set the pointer to the inserted node
            self.pointer = node

        # increase length as we have added a node
        self.length += 1

    def remove(self):
        """Remove the node at the pointer and return it."""
        # check if the list has any elements
        if self.length < 1:
            print("No elements to remove.")
            return None
        # get new left (left of the pointer)
        new_left = self.pointer.left
        # get new right (right of the pointer)
        new_right = self.pointer.right
        # get the node to remove
        node = self.pointer
        # relink the new_left and new_right with each other
        new_left.right = new_right
        new_right.left = new_left
        # decrease the node count
        self.length -= 1

        return node

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
            # to reduce the number of steps, take the value mod the length of the
            # list, it wraps around :)
            # modulo needs to be reduced by one as the node can't be counted (i.e. skipped over)
            # once we have started moving it (this simulates individual steps moving it)
            steps = ((-1 * n) % (self.length - 1)) + 1
        elif n > 0:
            f_move = self.shift_right
            steps = n % (self.length - 1)

        self.pointer = node
        # remove the node
        popped_node = self.remove()
        # move number of steps
        for _ in range(steps):
            f_move()
        # insert the node
        self.insert(popped_node)

    def __repr__(self) -> str:
        return f"Start: {self.start}, pointer: {self.pointer}, nodes: {self.length}"


@aoc_timer
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
        # store zero node
        if n == 0:
            zero_node = node

    # process the nodes and move each of them
    for i in nodes:
        node = nodes[i]
        ll.move_node(node, node.value)

    # calculate 1000th, 2000th and 3000th number after 0
    # we don't need to move 1000 times, just take the modulo with the
    # length of the linked list
    coord = 0
    for i in [1000, 2000, 3000]:
        pos = i % ll.length
        # set the pointer to the zero_node
        ll.pointer = zero_node
        # move by pos steps
        for _ in range(pos):
            ll.shift_right()
        # get the value
        coord += ll.pointer.value

    return coord


@aoc_timer
def part2(puzzle_input):
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
        # part 2, multiply node number by 811589153
        node = Node(n * 811589153)
        ll.insert(node)
        nodes[i] = node
        # store zero node
        if n == 0:
            zero_node = node

    # process the nodes and move each of them
    # part 2, mix 10 times
    for mix_round in range(10):
        for i in range(count_elements):
            node = nodes[i]
            ll.move_node(node, node.value)

    # calculate 1000th, 2000th and 3000th number after 0
    # we don't need to move 1000 times, just take the modulo with the
    # length of the linked list
    coord = 0
    for i in [1000, 2000, 3000]:
        pos = i % ll.length
        # set the pointer to the zero_node
        ll.pointer = zero_node
        # move by pos steps
        for _ in range(pos):
            ll.shift_right()
        # get the value
        coord += ll.pointer.value

    return coord


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/20.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 14:30  End: 17:20
# Part 2: Start: 17:20 End: 18:16

# Elapsed time to run part1: 0.61597 seconds.
# Part 1: 23321
# Elapsed time to run part2: 6.81438 seconds.
# Part 2: 1428396909280
