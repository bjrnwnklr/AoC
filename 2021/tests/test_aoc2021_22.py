"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_22 import load_input, part1, part2, Cube, overlap, intersection


class Test_AOC2021_22:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition, put the example in a 
    `test_n_n.txt` file in the `test` directory, and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_1(self):
        puzzle_input = load_input('testinput/22_1_1.txt')
        assert part1(puzzle_input) == 590784

    def test_1_2(self):
        puzzle_input = load_input('testinput/22_1_2.txt')
        assert part1(puzzle_input) == 39

    def test_overlap_2_1(self):
        """Test if the first two cubes from the first example have an overlap.

        on x=10..12,y=10..12,z=10..12
        on x=11..13,y=11..13,z=11..13
        """
        puzzle_input = load_input('testinput/22_1_2.txt')
        cubes = [Cube(x, *y) for x, y in puzzle_input]
        a = cubes[0]
        b = cubes[1]
        assert overlap(a, b) == True

    def test_volume_2_1(self):
        """Test volume of the first cube, which is 27.

        on x=10..12,y=10..12,z=10..12
        """
        puzzle_input = load_input('testinput/22_1_2.txt')
        cubes = [Cube(x, *y) for x, y in puzzle_input]
        a = cubes[0]
        assert a.volume() == 27

    def test_intersection_2_1(self):
        """Test the intersection of the first two cubes from the first example.

        They intersect, resulting in a Cube(11..12, 11..12, 11..12) with size 8.

        on x=10..12,y=10..12,z=10..12
        on x=11..13,y=11..13,z=11..13
        """
        puzzle_input = load_input('testinput/22_1_2.txt')
        cubes = [Cube(x, *y) for x, y in puzzle_input]
        a = cubes[0]
        b = cubes[1]
        c = intersection(a, b)
        assert c == Cube('off', 11, 12, 11, 12, 11, 12)
        assert c.volume() == 8

    def test_2_2(self):
        puzzle_input = load_input('testinput/22_1_2.txt')
        assert part2(puzzle_input) == 39

    def test_2_3(self):
        """Runs the part 2 solution on the puzzle 1 larger example input,
        but without the last two lines which have coordinates > 50.
        """
        puzzle_input = load_input('testinput/22_2_2.txt')
        assert part2(puzzle_input) == 590784

    def test_2_1(self):
        puzzle_input = load_input('testinput/22_2_1.txt')
        assert part2(puzzle_input) == 2758514936282235
