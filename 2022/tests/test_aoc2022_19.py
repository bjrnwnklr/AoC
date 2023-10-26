"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2022_19 import load_input, part1, part2, State, score


class Test_AOC2022_19:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition,
     put the example in a `test_n_n.txt` file in the `test` directory,
     and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_1(self):
        puzzle_input = load_input("testinput/19_1_1.txt")
        assert part1(puzzle_input) == 33

    # def test_2_1(self):
    #     puzzle_input = load_input('testinput/19_1_1.txt')
    #     assert part2(puzzle_input) == 1

    def test_score_1(self):
        blueprint = [1, 4, 2, 3, 14, 2, 7]
        a = State()
        a.minute = 3
        a.robots = [1, 2, 3, 4]
        a.materials = [1, 0, 0, 0]
        assert score(a, blueprint) == 5
        a.materials = [1, 1, 0, 0]
        assert score(a, blueprint) == 8
        a.materials = [1, 1, 1, 0]
        assert score(a, blueprint) == 28
        a.materials = [1, 7, 1, 0]
        assert score(a, blueprint) == 34
        a.materials = [1, 10, 0, 0]
        assert score(a, blueprint) == 17
