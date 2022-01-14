"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_23_str import load_input, movers, part1, part2, path_from_room_free, room_pos, target_room_free, to_string


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

    def test_1_target_room_free(self):
        """Test the target_room_free method for 'C.A..B..C.....DA.BD'.
        Expected results:
        'A': (True, 11) -> Row 2 is occupied by correct pod, row 1 is free
        'B': (True, 16) -> Row 1 and 2 are free
        'C': (False, -1) -> Row 1 is free and 2 is occupied by incorrect pod.
        'D': (False, -1) -> Row 1 and 2 are occupied by two correct pods
        """
        assert target_room_free('C.A..B..C.....DA.BD', 'A') == (True, 11)
        assert target_room_free('C.A..B..C.....DA.BD', 'B') == (True, 16)
        assert target_room_free('C.A..B..C.....DA.BD', 'C') == (False, -1)
        assert target_room_free('C.A..B..C.....DA.BD', 'D') == (False, -1)

    def test_1_path_from_room_free(self):
        """Test the path_from_room_free method for 'C....B..C..A..DA.BD'.
        Expected results:
        11: True -> Pod is on row 1
        17: True -> Pod is on row 2, row 1 is free
        18: False -> Row 1 is occupied 
        """
        assert path_from_room_free('C....B..C..A..DA.BD', 11) == True
        assert path_from_room_free('C....B..C..A..DA.BD', 17) == True
        assert path_from_room_free('C....B..C..A..DA.BD', 18) == False

    def test_2_path_from_room_free(self):
        """Test the path_from_room_free method for 'C....B..C..A..DA.BDABCDABCD'.
        Expected results:
        11: True -> Pod is on row 1
        17: True -> Pod is on row 2, row 1 is free
        18: False -> Row 1 is occupied 
        20: True -> Pod is on row 2 but 1 and 2 are free
        21: False -> Pod is on 2 but row 1 is occupied
        22: False -> Pod is on 2 but row 1 and 2 are occupied
        26: False -> Rows 1, 2, 3 are occupied
        """
        assert path_from_room_free('C....B..C..A..DA.BDABCDABCD', 11) == True
        assert path_from_room_free('C....B..C..A..DA.BDABCDABCD', 17) == True
        assert path_from_room_free('C....B..C..A..DA.BDABCDABCD', 18) == False
        assert path_from_room_free('C....B..C..A..DA.BDABCDABCD', 20) == True
        assert path_from_room_free('C....B..C..A..DA.BDABCDABCD', 21) == False
        assert path_from_room_free('C....B..C..A..DA.BDABCDABCD', 22) == False
        assert path_from_room_free('C....B..C..A..DA.BDABCDABCD', 26) == False

    def test_1_room_pos(self):
        """Test the room_pos method.
        Expected results:
        0: (0, 0) -> hallway
        10: (0, 10) -> hallway
        11: (1, 2) -> first room
        14: (1, 8) -> last room
        16: (2, 4) -> 2nd room
        21: (3, 6) -> 3rd room
        23: (4, 2) -> 1st room
        """
        assert room_pos(0) == (0, 0)
        assert room_pos(10) == (0, 10)
        assert room_pos(11) == (1, 2)
        assert room_pos(12) == (1, 4)
        assert room_pos(13) == (1, 6)
        assert room_pos(14) == (1, 8)
        assert room_pos(16) == (2, 4)
        assert room_pos(21) == (3, 6)
        assert room_pos(23) == (4, 2)

    # def test_2_1(self):
    #     puzzle_input = load_input('testinput/23_1_1.txt')
    #     assert part2(puzzle_input) == 1
