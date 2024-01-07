"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2023_24 import (
    load_input,
    part1,
    part2,
    part2_np_solve,
    part2_convergence,
)


class Test_AOC2023_24:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition,
     put the example in a `test_n_n.txt` file in the `test` directory,
     and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_1(self):
        puzzle_input = load_input("testinput/24_1_1.txt")
        assert part1(puzzle_input, 7, 27) == 2

    def test_2_1(self):
        puzzle_input = load_input("testinput/24_1_1.txt")
        assert part2(puzzle_input) == 47

    # def test_2_2(self):
    #     puzzle_input = load_input("testinput/24_1_1.txt")
    #     assert part2_np_solve(puzzle_input) == 47

    def test_2_3(self):
        puzzle_input = load_input("testinput/24_1_1.txt")
        assert part2_convergence(puzzle_input) == 47
