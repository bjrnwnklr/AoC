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

    def test_1_add_1(self):
        a, b = '[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]'
        assert add(a, b) == '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'

    def test_1_reduction_1(self):
        sn = '[[[[[9,8],1],2],3],4]'
        assert reduce(sn) == '[[[[0,9],2],3],4]'

    def test_1_reduction_2(self):
        sn = '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'
        assert reduce(sn) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

    def test_1_add_all_1(self):
        puzzle_input = load_input('testinput/18_1_1.txt')
        assert add_all_numbers(
            puzzle_input) == '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]'

    def test_1_add_all_2(self):
        puzzle_input = load_input('testinput/18_1_2.txt')
        assert add_all_numbers(
            puzzle_input) == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'

    def test_1_add_all_3(self):
        puzzle_input = load_input('testinput/18_1_3.txt')
        assert add_all_numbers(
            puzzle_input) == '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'

    def test_1_magnitude_1(self):
        puzzle_input = load_input('testinput/18_1_3.txt')
        assert part1(puzzle_input) == 4140

    # def test_2_1(self):
    #     puzzle_input = load_input('testinput/18_1_1.txt')
    #     assert part2(puzzle_input) == 1
