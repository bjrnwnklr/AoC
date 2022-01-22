"""Test the examples given in the puzzle to verify the solution is working."""

import pytest
# load the required functions from the actual solution
from solutions.aoc2021_24 import load_input, part1, part2, ALU


class Test_AOC2021_24:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition, put the example in a 
    `test_n_n.txt` file in the `test` directory, and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_input_1(self):
        """Test if input can be read. Expected that one 1 is in variable w"""
        puzzle_input = load_input('testinput/24_1_1.txt')
        alu = ALU(puzzle_input)
        alu.put_input((1, ))
        alu.run()
        assert alu.vars['w'] == 1

    def test_1_input_2(self):
        """Test if input can be read. Expected that ValueError is raised if no input in buffer."""
        puzzle_input = load_input('testinput/24_1_1.txt')
        alu = ALU(puzzle_input)
        with pytest.raises(ValueError):
            alu.run()

    def test_1_input_3(self):
        """Test if input can be read. Expected that ValueError is raised if 0 is provided in input."""
        puzzle_input = load_input('testinput/24_1_1.txt')
        alu = ALU(puzzle_input)
        with pytest.raises(ValueError):
            alu.put_input((0, ))

    def test_1_run_1(self):
        """Test the 2nd example program:

        Takes two input numbers, then sets z to 1 if the second input number is 
        three times larger than the first input number, or sets z to 0 otherwise.

        Expected outcomes:
        inp = 13 -> z == 1
        inp = 11 -> z == 0
        inp = 39 -> z == 1
        """
        puzzle_input = load_input('testinput/24_1_2.txt')
        for inp, res in zip([(1, 3), (1, 1), (3, 9)], [1, 0, 1]):
            alu = ALU(puzzle_input)
            alu.put_input(inp)
            alu.run()
            assert alu.vars['z'] == res

    # def test_2_1(self):
    #     puzzle_input = load_input('testinput/24_1_1.txt')
    #     assert part2(puzzle_input) == 1
