"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_18 import add_all_numbers, load_input, part1, part2, reduce, add, tokenize, add_all_numbers


class Test_AOC2021_18:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition, put the example in a 
    `test_n_n.txt` file in the `test` directory, and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_convert_1(self):
        puzzle_input = '[[[[[9,8],1],2],3],4]'
        assert tokenize(puzzle_input) == [
            '[', '[', '[', '[', '[', 9, ',', 8, ']', ',', 1, ']', ',', 2, ']', ',', 3, ']', ',', 4, ']']

    def test_1_magnitude_1(self):
        puzzle_input = load_input('testinput/18_1_3.txt')
        assert part1(puzzle_input) == 4140

    def test_2_largest_magnitude_1(self):
        puzzle_input = load_input('testinput/18_1_3.txt')
        assert part2(puzzle_input) == 3993
