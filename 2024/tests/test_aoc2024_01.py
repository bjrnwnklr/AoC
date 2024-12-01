"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2024_01 import load_input, part1, part2


class Test_AOC2024_01:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition,
     put the example in a `test_n_n.txt` file in the `test` directory,
     and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_1(self):
        puzzle_input = load_input("testinput/01_1_1.txt")
        assert part1(puzzle_input) == 11

    def test_2_1(self):
        puzzle_input = load_input("testinput/01_1_1.txt")
        assert part2(puzzle_input) == 31
