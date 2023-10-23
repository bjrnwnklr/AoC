"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2022_22 import (
    load_input,
    part1,
    part2,
    wrap_cube,
    Position,
    parse_map,
)


class Test_AOC2022_22:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition,
     put the example in a `test_n_n.txt` file in the `test` directory,
     and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    # def test_1_1(self):
    #     raw_map, instructions = load_input("testinput/22_1_1.txt")
    #     assert part1(raw_map, instructions) == 6032

    # def test_2_1(self):
    #     raw_map, instructions = load_input("testinput/22_1_1.txt")
    #     assert part2(raw_map, instructions) == 5031

    def test_2_1_wrap_1_3(self):
        raw_map, instructions = load_input("input/22.txt")
        grid = parse_map(raw_map)
        pos = Position(0, 50, 3)
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 150
        assert new_pos.col == 0
        pos = Position(0, 52, 3)
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 152
        assert new_pos.col == 0

    def test_2_1_wrap_1_2(self):
        raw_map, instructions = load_input("input/22.txt")
        grid = parse_map(raw_map)
        pos = Position(0, 50, 2)
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 149
        assert new_pos.col == 0
        pos = Position(10, 50, 2)
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 139
        assert new_pos.col == 0
        pos = Position(49, 50, 2)
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 100
        assert new_pos.col == 0

    def test_2_1_wrap_2_0(self):
        raw_map, instructions = load_input("input/22.txt")
        grid = parse_map(raw_map)
        pos = Position(0, 100, 0)
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 2
        assert new_pos.row == 149
        assert new_pos.col == 99
        pos = Position(10, 100, 0)
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 2
        assert new_pos.row == 139
        assert new_pos.col == 99
        pos = Position(49, 100, 0)
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 2
        assert new_pos.row == 100
        assert new_pos.col == 99
