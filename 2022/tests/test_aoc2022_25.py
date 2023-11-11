"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2022_25 import load_input, part1, part2, snafu_to_dec, dec_to_snafu


class Test_AOC2022_25:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition,
     put the example in a `test_n_n.txt` file in the `test` directory,
     and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_1(self):
        puzzle_input = load_input("testinput/25_1_1.txt")
        assert part1(puzzle_input) == "2=-1=0"

    def test_snafu_to_dec(self):
        sn = "1=-0-2"
        assert snafu_to_dec(sn) == 1747

    def test_dec_to_snafu(self):
        dn = 3
        assert dec_to_snafu(dn) == "1="
        dn = 4
        assert dec_to_snafu(dn) == "1-"
        dn = 8
        assert dec_to_snafu(dn) == "2="
        dn = 2022
        assert dec_to_snafu(dn) == "1=11-2"

    # def test_2_1(self):
    #     puzzle_input = load_input('testinput/25_1_1.txt')
    #     assert part2(puzzle_input) == 1
