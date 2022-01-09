"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_23 import load_input, part1, part2, Burrow


class Test_AOC2021_23:
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
        b = Burrow(puzzle_input)
        assert b.state() == '...........BCBDADCA'

    def test_1_locked(self):
        """Test locked status for example 1_1 (ABBDADCA). 

        pods[0] (A) is locked (1st row with A below)
        pods[1] (B) is not locked (B is correct column, but incorrect D below)
        pods[4] (A) and pods[6] (C) are locked since they are in the second row and in correct position.
        """
        puzzle_input = load_input('testinput/23_1_3.txt')
        b = Burrow(puzzle_input)
        assert b.pods[0].locked == True
        assert b.pods[1].locked == False
        assert b.pods[4].locked == True
        assert b.pods[6].locked == True

    # def test_2_1(self):
    #     puzzle_input = load_input('testinput/23_1_1.txt')
    #     assert part2(puzzle_input) == 1
