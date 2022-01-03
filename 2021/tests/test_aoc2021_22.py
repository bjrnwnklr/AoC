"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_22 import load_input, part1, part2


class Test_AOC2021_22:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition, put the example in a 
    `test_n_n.txt` file in the `test` directory, and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_1(self):
        puzzle_input = load_input('testinput/22_1_1.txt')
        assert part1(puzzle_input) == 590784

    def test_1_2(self):
        puzzle_input = load_input('testinput/22_1_2.txt')
        assert part1(puzzle_input) == 39

    def test_2_1(self):
        puzzle_input = load_input('testinput/22_2_1.txt')
        assert part2(puzzle_input) == 2758514936282235
