# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer
from dataclasses import dataclass


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


@dataclass
class CPU:
    X: int = 1
    cycle: int = 0
    signal_strength: int = 0

    def update_signal_strength(self):
        if self.cycle in CYCLES:
            self.signal_strength += self.X * self.cycle
            # print(f'{self}')

CYCLES = [20, 60, 100, 140, 180, 220]

# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    Find signal strength (X value * cycle) at
    - 20
    - 60
    - 100
    - 140
    - 180
    - 220 cycles
    Sum up for result
    """
    cpu = CPU()

    for line in puzzle_input:
        # print(f'[{cpu.cycle}] {line} ({cpu})')
        match line.split():
            case ["noop"]:
                cpu.cycle += 1
                # evaluate if we reached a cycle point
                cpu.update_signal_strength()

            case ["addx", val]:
                cpu.cycle += 1
                cpu.update_signal_strength()
                cpu.cycle += 1
                cpu.update_signal_strength()
                # x is only increased AFTER the cycle
                cpu.X += int(val)


    return cpu.signal_strength


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/10.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 11:25 End: 11:50
# Part 2: Start: 11:51 End:
