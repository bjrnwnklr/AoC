"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_23_astar import hallway_free, heuristic, load_input, move_to, movers, part1, part2, path_from_room_free, path_length, possible_moves, room_pos, target_room_free, to_string


class Test_AOC2021_23_STR:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition, put the example in a 
    `test_n_n.txt` file in the `test` directory, and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_state(self):
        """Test state for example 1_1 (BCBDADCA)"""
        puzzle_input = load_input('testinput/23_1_1.txt')
        assert to_string(puzzle_input) == '...........BCBDADCA'

    def test_1_movers(self):
        """Test the movers method for example 1_1. Should return 
        B, C, B, D from the first row of rooms to move, and
        (16, D) and (18, A) from the 2nd row as they are in the wrong
        room (even if there is a pod above them).
        """
        puzzle_input = load_input('testinput/23_1_1.txt')
        mo = movers(to_string(puzzle_input))
        assert mo == [11, 12, 13, 14, 16, 18]

    def test_2_movers(self):
        """Test the movers method for '.A...B......B.DACCD' Should return 
        A, B from the hallway, B from the first row of rooms to move.
        """
        mo = movers('.A...B......B.DACCD')
        assert mo == [1, 5, 12, 16]

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

    def test_1_hallway_free(self):
        """Test the hallway_free method with '.A...B......B.DACCD'.

        #############
        #.A...B.....#
        ###.#B#.#D###
          #A#C#C#D#
          #########

        Expected results:
        (1, 2) = True
        (1, 10) = False
        (11, 14) = False
        (15, 14) = False
        (15, 12) = True
        (15, 0) = False
        """
        assert hallway_free('.A...B......B.DACCD', 1, 2) == True
        assert hallway_free('.A...B......B.DACCD', 1, 10) == False
        assert hallway_free('.A...B......B.DACCD', 11, 14) == False
        assert hallway_free('.A...B......B.DACCD', 15, 14) == False
        assert hallway_free('.A...B......B.DACCD', 15, 12) == True
        assert hallway_free('.A...B......B.DACCD', 15, 0) == False

    def test_1_path_length(self):
        """Test the path_length method.

        Expected results:
        (0, 0) = 0
        (0, 10) = 10
        (0, 11) = 3
        (11, 0) = 3
        (15, 11) = 1
        (11, 12) = 4
        (15, 16) = 6
        """
        assert path_length(0, 0) == 0
        assert path_length(0, 10) == 10
        assert path_length(0, 11) == 3
        assert path_length(11, 0) == 3
        assert path_length(15, 11) == 1
        assert path_length(11, 12) == 4
        assert path_length(15, 16) == 6

    def test_1_possible_moves(self):
        """Test the possible_moves method '.A...B......B.DACCD'.

        #############
        #.A...B.....#
        ###.#B#.#D###
          #A#C#C#D#
          #########

        Expected results:
        1 (A): [(2, 11)] -> can only move to the target room for A
        5 (B): [] -> no possible move as target room for B is occupied
        16 (C): [] -> no possible move as exit from room is blocked
        12 (B): [(20, 3)] -> should only be able to move to position 3
        14 (D): [(2000, 7), (2000, 9), (3000, 10)] -> theoretically not able to move, but possible_moves does not check that.
        """
        burrow = '.A...B......B.DACCD'
        assert possible_moves(burrow, 1) == [(2, 11)]
        assert possible_moves(burrow, 5) == []
        assert possible_moves(burrow, 16) == []
        assert possible_moves(burrow, 12) == [(20, 3)]
        assert possible_moves(burrow, 14) == [(2000, 7), (2000, 9), (3000, 10)]

    def test_1_move_to(self):
        """Test moving a pod from to and returning an updated burrow string.

        '.A...B......B.DACCD'

        Expected results:
        (0, 1) = 'A....B......B.DACCD' -> bit of an odd case, as we are moving a Dot to A but should still work
        (1, 0) = 'A....B......B.DACCD' -> Move of A to the left
        (12, 10) = '.A...B....B...DACCD' -> Move from row 1 to hallway
        (1, 11) = '.....B.....AB.DACCD' -> Move A into room 11
        """
        burrow = '.A...B......B.DACCD'
        assert move_to(burrow, 0, 1) == 'A....B......B.DACCD'
        assert move_to(burrow, 1, 0) == 'A....B......B.DACCD'
        assert move_to(burrow, 12, 10) == '.A...B....B...DACCD'
        assert move_to(burrow, 1, 11) == '.....B.....AB.DACCD'

    def test_1_heuristic(self):
        """Test the heuristic function to get distance from the target state.
        '.A...B......B.DACCD'.

        #############
        #.A...B.....#
        ###.#B#.#D###
          #A#C#C#D#
          #########

        Expected result:
        A: 1
        B: 10
        B: 0
        D: 0
        A: 0
        C: 200
        C: 0
        D: 0
        Total: 211

        '...........DABCBADC'

        #############
        #...........#
        ###D#A#B#C###
          #B#A#D#C#
          #########

        Expected result:
        D: 6000
        A: 2
        B: 20
        C: 200
        B: 20
        A: 2
        D: 2000
        C: 200
        Total: 8444
        """
        assert heuristic('.A...B......B.DACCD') == 211
        assert heuristic('...........DABCBADC') == 8444

    def test_1_1(self):
        puzzle_input = load_input('testinput/23_1_1.txt')
        assert part1(puzzle_input) == 12521

    def test_1_2(self):
        puzzle_input = load_input('testinput/23_1_2.txt')
        assert part1(puzzle_input) == 13336

    # def test_2_1(self):
    #     puzzle_input = load_input('testinput/23_1_1.txt')
    #     assert part2(puzzle_input) == 1
