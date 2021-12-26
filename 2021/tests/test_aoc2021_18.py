"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_18 import load_input, part1, part2, reduce, add, convert


class Test_AOC2021_18:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition, put the example in a 
    `test_n_n.txt` file in the `test` directory, and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_convert_1(self):
        puzzle_input = '[[[[[9,8],1],2],3],4]'
        assert convert(puzzle_input) == [[[[[9, 8], 1], 2], 3], 4]

    def test_1_add_1(self):
        a, b = '[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]'
        sn_a = convert(a)
        sn_b = convert(b)
        assert add(sn_a, sn_b) == [
            [[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]

    def test_1_reduction_1(self):
        puzzle_input = '[[[[[9,8],1],2],3],4]'
        assert reduce(
            puzzle_input) == '[[[[0,9],2],3],4]'

    def test_1_reduction_2(self):
        puzzle_input = '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'
        assert reduce(
            puzzle_input) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

    # def test_1_1(self):
    #     puzzle_input = load_input('testinput/18_1_1.txt')
    #     assert part1(
    #         puzzle_input) == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'

    # def test_2_1(self):
    #     puzzle_input = load_input('testinput/18_1_1.txt')
    #     assert part2(puzzle_input) == 1
