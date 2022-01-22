# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer
import logging


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

    def decode_instruction(self, instr: str) -> tuple[str, int]:
        """Decodes a string instruction and returns a tuple containing the instruction
        and values/variables, e.g. 'inp x' -> ('inp', 'x')."""
        match instr.split():
            case ['inp', v]:
                result = ('inp', v)
            case [ic, a, b]:
                assert ic in ['add', 'mul', 'div', 'mod', 'eql']
                assert a in ['w', 'x', 'y', 'z']
                if b in ['w', 'x', 'y', 'z']:
                    result = (ic, a, b)
                else:
                    result = (ic, a, int(b))

        return result

    def put_input(self, inp: int) -> None:
        """Load an integer into the input_buffer by splitting it into individual numbers. Checks if
        input is in [1-9]."""
        inp_list = list(map(int, list(str(inp))))
        if not all(x in range(1, 10) for x in inp_list):
            raise ValueError(f'Input value not in [1-9]: {inp}.')

        self.input_buffer.extend(inp_list)

    def run(self) -> None:
        """Run an ALU program from top to bottom."""
        logging.debug(f'Running program of length {len(self.pgm)}.')
        for i, raw_instr in enumerate(self.pgm):
            logging.debug(f'[{i:04}]: {raw_instr}')
            instr = self.decode_instruction(raw_instr)
            match instr:
                case ('inp', v):
                    if self.input_buffer:
                        self.vars[v] = self.input_buffer.pop(0)
                    else:
                        raise ValueError(
                            f'Expected input, but input buffer is empty: {instr=}')
                case ('add', a, b):
                    pass
                case ('mul', a, b):
                    pass
                case ('div', a, b):
                    pass
                case ('mod', a, b):
                    pass
                case ('eql', a, b):
                    pass


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

    alu = ALU(puzzle_input)
    alu.put_input(11111111111111)
    return 1


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

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
