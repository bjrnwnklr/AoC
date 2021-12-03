# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict

def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `test/test1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(list(map(int, list(line.strip()))))

    return puzzle_input


def gamma(l):
    # how many lines in the list - used to calc the most frequent bit
    n = len(l)
    columns = list(zip(*l))
    g = [
        1 if sum(c) > n // 2 else 0 for c in columns
    ]
    return ''.join(str(x) for x in g)


def epsilon(g):
    return ''.join('1' if x == '0' else '0' for x in g)


def bin_to_int(b):
    return int(b, base=2)


def most_common_bit(l, pos):
    n = len(l)
    col = list(zip(*l))[pos]
    # TODO: This is incorrect e.g. for list with 7 elements and 3 1s and 4 0s
    # this returns 1 (3 >= 7//2 = 3)
    return 1 if sum(col) >= n // 2 else 0


def rating(l, r_type='oxy'):
    pos = 0
    while len(l) > 1:
        bit_criteria = most_common_bit(l, pos)
        if r_type == 'co2':
            bit_criteria = 0 if bit_criteria == 1 else 1
        l = [x for x in l if x[pos] == bit_criteria]
        print(f'{pos=}, {bit_criteria=}, {l=}')
        pos += 1

    return ''.join(str(x) for x in l[0])


def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    g = gamma(puzzle_input)
    e = epsilon(g)

    return bin_to_int(g) * bin_to_int(e)


def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    oxy = rating(puzzle_input[:])
    co2 = rating(puzzle_input[:], 'co2')

    return bin_to_int(oxy) * bin_to_int(co2)


if __name__ == '__main__':
    # read the puzzle input
    # puzzle_input = load_input('input.txt')
    puzzle_input = load_input('test/test1_1.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 19:11, End: 19:29
# Part 2: Start: 19:30, End:
