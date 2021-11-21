# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict

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
        # return a list of the letters of the polymer - so read one line, then turn that into
        # a list
        line = f.readline().strip()

    return line


def react(puzzle_input):
    remaining_polymer = []
    polymer = list(puzzle_input)

    for p in polymer:
        if remaining_polymer and ((remaining_polymer[-1].lower() == p.lower())
                                  & (remaining_polymer[-1] != p)):
            remaining_polymer.pop()
        else:
            remaining_polymer.append(p)

    return ''.join(remaining_polymer)


def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    Args:
        puzzle_input (List): Typically a list of the input values from the input.txt puzzle input.

    Returns:
        Depends...: Typically an Integer value, but often also a String - this can be used on adventofcode 
        as the answer to the puzzle.
    """
    # parse through the list one by one and see if any of the pieces react to the current
    # unit
    remaining_polymer = react(puzzle_input)
    return len(remaining_polymer)


def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    Args:
        puzzle_input (List): Typically a list of the input values from the input.txt puzzle input.

    Returns:
        Depends...: Typically an Integer value, but often also a String - this can be used on adventofcode 
        as the answer to the puzzle.
    """
    # find each existing unit in the polymer and remove it, then process the polymer
    units = set(puzzle_input.lower())
    best_unit = ''
    shortest_polymer = puzzle_input
    for u in units:
        translator = str.maketrans('', '', f'{u}{u.upper()}')
        p = puzzle_input.translate(translator)
        polymer = react(list(p))

        if len(polymer) < len(shortest_polymer):
            shortest_polymer = polymer
            best_unit = u

    return len(shortest_polymer)


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')


# Part 1: 10180

# Part 2: 5668, Remove unit: c
