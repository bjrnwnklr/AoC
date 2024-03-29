"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2022_15 import load_input, part1, part2


class Test_AOC2022_15:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition,
     put the example in a `test_n_n.txt` file in the `test` directory,
     and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_1(self):
        """
        In this example, in the row where y=10, there are 26 positions where a beacon cannot be present.
        """
        puzzle_input = load_input("testinput/15_1_1.txt")
        assert part1(puzzle_input, y=10) == 26

    def test_2_1(self):
        puzzle_input = load_input("testinput/15_1_1.txt")
        assert part2(puzzle_input, max_xy=20) == 56000011
