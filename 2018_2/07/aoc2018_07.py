# Load any required modules. Most commonly used:

# import re
from collections import defaultdict


def load_input(f_name):
    """Loads the puzzle input from the specified file. Specify the relative path 
    if loading files from a subdirectory, e.g. for loading test inputs, specify
    `test/test1_1.txt`.

    Depending on the puzzle, change how the lines in the file are parsed, what format
    the extracted values have etc.

    Args:
        f_name (String): File name of the input file.

    Returns:
        List: A list of the inputs read in.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            words = line.strip().split()
            puzzle_input.append((words[1], words[7]))

    return puzzle_input


def toposort(pi):
    pre = defaultdict(list)
    boxes = set()
    for a, b in pi:
        boxes.add(a)
        boxes.add(b)
        pre[b].append(a)

    # find any elements that don't have predecessors - this is the element to start with
    baselist = set(c for c in boxes if c not in pre)
    result = []
    while baselist:
        # take the alphabetically first element of the baselist - it doesnt have
        # any predecessors so it is the next box to process
        next_box = sorted(baselist)[0]
        baselist.remove(next_box)
        result.append(next_box)

        for box in pre:
            # remove the box from all predecessors since we have cleared the dependency
            if next_box in pre[box]:
                pre[box].remove(next_box)
            # generate the new baselist - all boxes in predecessor that have an empty list
            # i.e. are not depending on any predecessor
            if box not in result and not pre[box]:
                baselist.add(box)

    return ''.join(result)


def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    Args:
        puzzle_input (List): Typically a list of the input values from the input.txt puzzle input.

    Returns:
        Depends...: Typically an Integer value, but often also a String - this can be used on adventofcode 
        as the answer to the puzzle.
    """
    return toposort(puzzle_input)


def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    Args:
        puzzle_input (List): Typically a list of the input values from the input.txt puzzle input.

    Returns:
        Depends...: Typically an Integer value, but often also a String - this can be used on adventofcode 
        as the answer to the puzzle.
    """
    # Add code here

    return 1


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')
