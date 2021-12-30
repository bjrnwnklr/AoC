# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `test/test1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


class Submarine:
    def __init__(self) -> None:
        self.horizontal = 0
        self.depth = 0
        self.aim = 0

    def move(self, instruction):
        match instruction.split():
            case ('forward', n):
                self.horizontal += int(n)
            case ('down', n):
                self.depth += int(n)
            case ('up', n):
                self.depth -= int(n)

    def move_2(self, instruction):
        match instruction.split():
            case ('forward', n):
                self.horizontal += int(n)
                self.depth += self.aim * int(n)
            case ('down', n):
                self.aim += int(n)
            case ('up', n):
                self.aim -= int(n)

    def get_pos(self):
        return (self.horizontal, self.depth)

    def get_result(self):
        return self.horizontal * self.depth


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    sub = Submarine()
    for instruction in puzzle_input:
        sub.move(instruction)

    return sub.get_result()


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    sub = Submarine()
    for instruction in puzzle_input:
        sub.move_2(instruction)

    return sub.get_result()


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/02.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')


# Part 1: Start: 18:50, End: 19:01
# Part 2: Start: 19:02, End: 19:05


# Part 1: 1989014
# Part 2: 2006917119
