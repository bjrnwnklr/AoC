"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_12 import load_input, part1, part2


class Test_AOC2021_12:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition, put the example in a 
    `test_n_n.txt` file in the `test` directory, and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_1(self):
        puzzle_input = load_input('testinput/12_1_1.txt')
        assert part1(puzzle_input) == 10

    def test_1_2(self):
        puzzle_input = load_input('testinput/12_1_2.txt')
        assert part1(puzzle_input) == 19

    def test_1_3(self):
        puzzle_input = load_input('testinput/12_1_3.txt')
        assert part1(puzzle_input) == 226

    def test_2_1(self):
        puzzle_input = load_input('testinput/12_1_1.txt')
        assert part2(puzzle_input) == 36

    def test_2_2(self):
        puzzle_input = load_input('testinput/12_1_2.txt')
        assert part2(puzzle_input) == 103

    def test_2_3(self):
        puzzle_input = load_input('testinput/12_1_3.txt')
        assert part2(puzzle_input) == 3509
