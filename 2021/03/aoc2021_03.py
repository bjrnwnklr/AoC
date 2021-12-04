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


def bin_to_int(l):
    b = ''.join(str(x) for x in l)
    return int(b, base=2)


def most_common_bit(l, pos):
    ones = sum(
        x[pos] == 1 for x in l
    )

    zeros = sum(
        x[pos] == 0 for x in l
    )

    return 1 if ones > zeros else 0

def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    # gamma
    g = [most_common_bit(puzzle_input[:], i) for i in range(len(puzzle_input[0]))]
    e = [1 if x == 0 else 0 for x in g]

    return bin_to_int(g) * bin_to_int(e)


def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
   
    # calculate oxy rating (most common bit in position, 1 in a tie)
    l = puzzle_input[:]
    pos = 0
    while len(l) > 1:
        ones = [x for x in l if x[pos] == 1]
        zeros = [x for x in l if x[pos] == 0]
        if len(ones) >= len(zeros):
            l = ones
        else:
            l = zeros
        
        pos += 1

    oxy = l[0]

    # calculate co2 rating (least common bit in position, 0 in a tie)
    l = puzzle_input[:]
    pos = 0
    while len(l) > 1:
        ones = [x for x in l if x[pos] == 1]
        zeros = [x for x in l if x[pos] == 0]
        if len(zeros) <= len(ones):
            l = zeros
        else:
            l = ones

        pos += 1

    co2 = l[0]

    return bin_to_int(oxy) * bin_to_int(co2)


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 19:11, End: 19:29
# Part 2: Start: 19:30, End: 9:59 (next day)

# Part 1: 1131506
# Part 2: 7863147
