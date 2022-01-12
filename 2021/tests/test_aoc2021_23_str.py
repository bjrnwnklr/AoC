"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_23_str import load_input, movers, part1, part2, to_string


class Test_AOC2021_23_STR:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition, put the example in a 
    `test_n_n.txt` file in the `test` directory, and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    # def test_1_1(self):
    #     puzzle_input = load_input('testinput/23_1_1.txt')
    #     assert part1(puzzle_input) == 12521

    # def test_1_2(self):
    #     puzzle_input = load_input('testinput/23_1_2.txt')
    #     assert part1(puzzle_input) == 13336

    def test_1_state(self):
        """Test state for example 1_1 (BCBDADCA)"""
        puzzle_input = load_input('testinput/23_1_1.txt')
        assert to_string(puzzle_input) == '...........BCBDADCA'

    def test_1_movers(self):
        """Test the movers method for example 1_1. Should return 
        B, C, B, D from the first row of rooms to move.
        """
        puzzle_input = load_input('testinput/23_1_1.txt')
        mo = movers(to_string(puzzle_input))
        assert mo == [(11, 'B'), (12, 'C'), (13, 'B'), (14, 'D')]

    def test_2_movers(self):
        """Test the movers method for '..A..B......B.DACCD' Should return 
        A, B from the hallway, B from the first row of rooms to move.
        """
        mo = movers('..A..B......B.DACCD')
        assert mo == [(2, 'A'), (5, 'B'), (12, 'B')]

    # def test_2_1(self):
    #     puzzle_input = load_input('testinput/23_1_1.txt')
    #     assert part2(puzzle_input) == 1
