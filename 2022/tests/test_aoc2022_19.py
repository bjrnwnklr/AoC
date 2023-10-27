"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2022_19 import load_input, part1, part2, minutes_to_build, recipes


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

    def test_1_minutes_to_build(self):
        blueprint = [1, 4, 2, 3, 14, 2, 7]
        # test if an ore robot can be built from no materials
        state = (0, [1, 0, 0, 0], [0, 0, 0, 0])
        recipe = recipes(blueprint)
        assert minutes_to_build(recipe, state, 0) == 5
        # build an ore robot when enough materials exist
        state = (0, [1, 0, 0, 0], [4, 0, 0, 0])
        recipe = recipes(blueprint)
        assert minutes_to_build(recipe, state, 0) == 1
        # build an obsidian robot with no materials
        state = (0, [1, 1, 0, 0], [0, 0, 0, 0])
        recipe = recipes(blueprint)
        assert minutes_to_build(recipe, state, 2) == 15
        # build an obsidian robot with some materials
        state = (0, [1, 1, 0, 0], [3, 10, 0, 0])
        recipe = recipes(blueprint)
        assert minutes_to_build(recipe, state, 2) == 5
        # build an obsidian robot with surplus materials
        state = (0, [1, 1, 0, 0], [4, 15, 0, 0])
        recipe = recipes(blueprint)
        assert minutes_to_build(recipe, state, 2) == 1
        # build an obsidian robot with lots of robots
        state = (0, [2, 3, 0, 0], [0, 1, 0, 0])
        recipe = recipes(blueprint)
        assert minutes_to_build(recipe, state, 2) == 6
