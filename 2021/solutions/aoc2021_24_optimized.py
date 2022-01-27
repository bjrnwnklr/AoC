# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
from utils.aoctools import aoc_timer
import logging

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
def part1():
    """Solve part 1. Return the required output value."""
    return solve(False)


@aoc_timer
def part2():
    """Solve part 2. Return the required output value."""
    return solve(True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Solve part 1 and print the answer
    p1 = part1()
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2()
    print(f'Part 2: {p2}')

# Part 1: Start: 17:15 End:
# Part 2: Start:  End:
