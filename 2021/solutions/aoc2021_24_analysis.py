# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer
from decimal import DivisionByZero
import logging
from itertools import product


class ALU:
    def __init__(self, pgm: list[str]) -> None:
        logging.debug(
            f'Initializing new ALU with program of length {len(pgm)}.')
        self.pgm = pgm
        self.vars = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0
        }
        self.input_buffer = []

    def put_input(self, inp: int) -> None:
        """Load a list of integers into the input buffer."""
        if not all(x in range(1, 10) for x in inp):
            raise ValueError(f'Input value not in [1-9]: {inp}.')

        self.input_buffer.extend(inp)

    def get_val(self, b) -> int:
        """Return the value of b, which is either an int value, or the value stored in variable 'b'."""
        return self.vars[b] if b in self.vars else b

    def run(self, start: int = 0, stop: int = None) -> None:
        """Run an ALU program from top to bottom.

        `start` and `stop` can be used to run only the lines between `start` and `stop` (including `start` and `stop`).
        """
        if stop == None:
            stop = len(self.pgm)
        logging.debug(f'Running program segment [{start}:{stop + 1}].')
        for i, instr in enumerate(self.pgm[start:stop + 1], start):
            logging.debug(f'[{i:04}]: {instr} - {self.vars}')
            match instr:
                case ('inp', v):
                    if self.input_buffer:
                        self.vars[v] = self.input_buffer.pop(0)
                    else:
                        raise ValueError(
                            f'Expected input, but input buffer is empty: {instr=}')
                case ('add', a, b):
                    b_val = self.get_val(b)
                    self.vars[a] += b_val
                case ('mul', a, b):
                    b_val = self.get_val(b)
                    self.vars[a] *= b_val
                case ('div', a, b):
                    b_val = self.get_val(b)
                    if b_val == 0:
                        raise DivisionByZero(
                            f'Trying to divide by zero: {instr=}')
                    self.vars[a] = self.vars[a] // b_val
                case ('mod', a, b):
                    b_val = self.get_val(b)
                    if self.vars[a] < 0 or b_val <= 0:
                        raise DivisionByZero(
                            f'Modulo with zero value: {instr=}')
                    self.vars[a] %= b_val
                case ('eql', a, b):
                    b_val = self.get_val(b)
                    self.vars[a] = 1 if self.vars[a] == b_val else 0


def pre_process_pgm(raw_pgm: list[str]):
    """Pre process a program by splitting each line into parts and converting any numbers to int."""
    pgm = []
    for raw_instr in raw_pgm:
        instr = raw_instr.split()
        match instr:
            case ('inp', v):
                pgm.append(('inp', v))
            case (c, a, b):
                if b in ['w', 'x', 'y', 'z']:
                    pgm.append((c, a, b))
                else:
                    pgm.append((c, a, int(b)))

    return pgm


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    pgm = pre_process_pgm(puzzle_input)

    # run only lines 0-17 (first segment processing the first digit)
    start = 108
    stop = 125

    # load variables with this starting value:
    # (1, 6, 9, 9, 5, 9)
    # {'w': 9, 'x': 0, 'y': 0, 'z': 99756}
    load_vars = {'w': 9, 'x': 0, 'y': 0, 'z': 99756}

    result = 0
    for p in range(1, 10):
        # for p in range(1, 10):
        alu = ALU(pgm)
        for k, v in load_vars.items():
            alu.vars[k] = v
        alu.put_input((p, ))
        alu.run(start, stop)
        if alu.vars['z'] == 0:
            logging.info(f'Valid model number: {p}. {alu.vars=}')
            result = p
        else:
            logging.info(f'Invalid model number: {p}. {alu.vars=}')
    return result


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)

    logging.basicConfig(level=logging.INFO,
                        filename='24_segments.log', filemode='w')

    # read the puzzle input
    puzzle_input = load_input('input/24.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 17:15 End:
# Part 2: Start:  End:
