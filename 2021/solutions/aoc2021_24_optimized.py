# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
from utils.aoctools import aoc_timer
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


# parameters contain:
# line 4 (div z 1)
# line 5 (add x 12)
# line 15 (add y 4)
params = {
    0: [1, 12, 4],
    1: [1, 11, 11],
    2: [1, 13, 5],
    3: [1, 11, 11],
    4: [1, 14, 14],
    5: [26, -10, 7],
    6: [1, 11, 11],
    7: [26, -9, 4],
    8: [26, -3, 6],
    9: [1, 13, 5],
    10: [26, -5, 9],
    11: [26, -10, 12],
    12: [26, -4, 14],
    13: [26, -5, 14]
}


def segment_func(seg: int, w_val: int, z_val: int) -> tuple[int]:
    """Process a segment of the ALU code.

    - inp w
    - mul x 0
    - add x z
    - mod x 26
    * div z 1
    * add x 12
    - eql x w
    - eql x 0 # this line reverses the results of eql x w, so basically not(eql x w)
    - mul y 0
    * add y 25
    - mul y x
    * add y 1
    - mul z y
    - mul y 0
    - add y w
    * add y 4
    - mul y x
    - add z y
    """

    z4, x5, y15 = params[seg]
    x = (z_val % 26) + x5
    z = z_val // z4
    x = 1 if x != w_val else 0
    y = (x * 25) + 1
    z *= y
    y = (w_val + y15) * x
    z += y

    return (y, z)


def solve(part2=False):
    """Solve the puzzle by running through the program and analysing segment output.

    `part2` parameter defines if the solution is run for part 1 (highest number) or part 2 (lowest
    number).
    """
    segment = 0
    result = 0
    # dict[segment: int] = defaultdict[z]: inputnumber: int
    segment_output = {-1: {0: 0}}

    while segment < 14:
        current_segment = defaultdict(int)
        prior_segment = segment_output[segment - 1]
        reduce = True if segment in [5, 7, 8, 10, 11, 12, 13] else False
        for old_z in prior_segment:
            r = range(9, 0, -1) if part2 else range(1, 10)
            for p in r:
                new_input = prior_segment[old_z] * 10 + p
                new_y, new_z = segment_func(segment, p, old_z)
                if not reduce or new_y == 0:
                    current_segment[new_z] = new_input
                if new_z == 0:
                    logging.info(
                        f'Valid model number: {new_input}. {new_y=} {new_z=}')
                    result = new_input
        logging.info(
            f'Segment {segment} processed. {len(current_segment)} unique z values.')
        segment_output[segment] = current_segment
        segment += 1

    return result


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    return solve(False)


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    return solve(True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # logging.basicConfig(level=logging.INFO,
    #                     filename='24_segments.log', filemode='w')

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
