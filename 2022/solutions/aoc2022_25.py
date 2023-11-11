# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


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

    # Extract ints from the input
    #
    # signed ints
    # regex = re.compile(r"(-?\d+)")
    #
    # unsigned ints
    # regex = re.compile(r"(\d+)")
    #
    # with open(f_name, "r") as f:
    #     puzzle_input = []
    #     for line in f.readlines():
    #         matches = regex.findall(line.strip())
    #         if matches:
    #             puzzle_input.append(list(map(int, matches)))

    return puzzle_input


snafu_dec = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
dec_snafu = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}


def snafu_to_dec(sn):
    """Convert a number from SNAFU to decimal."""
    dec = 0
    for i, n in enumerate(sn[::-1]):
        dec += snafu_dec[n] * 5**i
    return dec


def dec_to_snafu(dn):
    """Convert SNAFU number to decimal."""
    # this is tricky but can be done similar to
    # converting from base 10 to base 5 by taking the
    # factor and remainder from dividing by 5 and
    # increasing the factor by 1 if a remainder > 2 is
    # found. The remainder is then decreased by 5 to
    # give the negative increment for this position.

    # base 5 of a decimal number n is
    # a_n * 5**n + a_(n-1) * 5**(n-1) + .. + a_0 * 5**0
    # the base 5 is then expressed as "a_n a_(n-1) .. a_0"
    result = []
    while dn != 0:
        r = dn % 5
        dn = dn // 5
        if r > 2:
            dn += 1
            r -= 5
        result.append(dec_snafu[r])

    return "".join(result[::-1])


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    # SNAFU numbers:
    # - digits are multiples of 5
    # - numbers are
    #   2 == 2
    #   1 == 1
    #   0 == 0
    #   - == -1
    #   = == -2

    # convert all SNAFU input numbers to decimal and sum up
    dec_sum = sum(snafu_to_dec(sn) for sn in puzzle_input)
    # convert back to SNAFU number
    snafu = dec_to_snafu(dec_sum)

    return snafu


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/25.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")


# Part 1: Start: 17:21 End: 18:30

# Elapsed time to run part1: 0.00019 seconds.
# Part 1: 2-0==21--=0==2201==2
