"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2022_22 import (
    load_input,
    part1,
    part2,
    wrap_cube,
    Position,
    parse_map,
    which_side,
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
        assert which_side(pos) == 1
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 150
        assert new_pos.col == 0
        pos = Position(0, 52, 3)
        assert which_side(pos) == 1
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 152
        assert new_pos.col == 0

    def test_2_1_wrap_1_2(self):
        raw_map, instructions = load_input("input/22.txt")
        grid = parse_map(raw_map)
        pos = Position(0, 50, 2)
        assert which_side(pos) == 1
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 149
        assert new_pos.col == 0
        pos = Position(10, 50, 2)
        assert which_side(pos) == 1
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 139
        assert new_pos.col == 0
        pos = Position(49, 50, 2)
        assert which_side(pos) == 1
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 100
        assert new_pos.col == 0

    def test_2_1_wrap_2_3(self):
        raw_map, instructions = load_input("input/22.txt")
        grid = parse_map(raw_map)
        pos = Position(0, 100, 3)
        assert which_side(pos) == 2
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 3
        assert new_pos.row == 199
        assert new_pos.col == 0
        pos = Position(0, 110, 3)
        assert which_side(pos) == 2
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 3
        assert new_pos.row == 199
        assert new_pos.col == 10
        pos = Position(0, 149, 3)
        assert which_side(pos) == 2
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 3
        assert new_pos.row == 199
        assert new_pos.col == 49

    def test_2_1_wrap_2_0(self):
        raw_map, instructions = load_input("input/22.txt")
        grid = parse_map(raw_map)
        pos = Position(0, 149, 0)
        assert which_side(pos) == 2
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 2
        assert new_pos.row == 149
        assert new_pos.col == 99
        pos = Position(10, 149, 0)
        assert which_side(pos) == 2
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 2
        assert new_pos.row == 139
        assert new_pos.col == 99
        pos = Position(49, 149, 0)
        assert which_side(pos) == 2
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 2
        assert new_pos.row == 100
        assert new_pos.col == 99

    def test_2_1_wrap_2_1(self):
        raw_map, instructions = load_input("input/22.txt")
        grid = parse_map(raw_map)
        pos = Position(49, 100, 1)
        assert which_side(pos) == 2
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 2
        assert new_pos.row == 50
        assert new_pos.col == 99
        pos = Position(49, 110, 1)
        assert which_side(pos) == 2
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 2
        assert new_pos.row == 60
        assert new_pos.col == 99
        pos = Position(49, 149, 1)
        assert which_side(pos) == 2
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 2
        assert new_pos.row == 99
        assert new_pos.col == 99

    def test_2_1_wrap_3_2(self):
        raw_map, instructions = load_input("input/22.txt")
        grid = parse_map(raw_map)
        pos = Position(50, 50, 2)
        assert which_side(pos) == 3
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 1
        assert new_pos.row == 100
        assert new_pos.col == 0
        pos = Position(60, 50, 2)
        assert which_side(pos) == 3
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 1
        assert new_pos.row == 100
        assert new_pos.col == 10

    def test_2_1_wrap_3_0(self):
        raw_map, instructions = load_input("input/22.txt")
        grid = parse_map(raw_map)
        pos = Position(50, 99, 0)
        assert which_side(pos) == 3
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 3
        assert new_pos.row == 49
        assert new_pos.col == 100
        pos = Position(60, 99, 0)
        assert which_side(pos) == 3
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 3
        assert new_pos.row == 49
        assert new_pos.col == 110

    def test_2_1_wrap_4_3(self):
        raw_map, instructions = load_input("input/22.txt")
        grid = parse_map(raw_map)
        pos = Position(100, 0, 3)
        assert which_side(pos) == 4
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 50
        assert new_pos.col == 50
        pos = Position(100, 10, 3)
        assert which_side(pos) == 0
        new_pos = wrap_cube(pos, grid)
        assert new_pos.facing == 0
        assert new_pos.row == 60
        assert new_pos.col == 50
