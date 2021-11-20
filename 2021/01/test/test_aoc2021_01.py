from aoc2021_01 import load_input, part1, part2


class Test202101:

    def test_1_1(self):
        puzzle_input = load_input('test/test1_1.txt')
        assert part1(puzzle_input) == 3

    def test_1_2(self):
        puzzle_input = load_input('test/test1_2.txt')
        assert part1(puzzle_input) == 3

    def test_1_3(self):
        puzzle_input = load_input('test/test1_3.txt')
        assert part1(puzzle_input) == 0

    def test_1_4(self):
        puzzle_input = load_input('test/test1_4.txt')
        assert part1(puzzle_input) == -6

    def test_2_1(self):
        puzzle_input = load_input('test/test1_1.txt')
        assert part2(puzzle_input) == 2

    def test_2_2(self):
        puzzle_input = load_input('test/test2_2.txt')
        assert part2(puzzle_input) == 0

    def test_2_3(self):
        puzzle_input = load_input('test/test2_3.txt')
        assert part2(puzzle_input) == 10

    def test_2_4(self):
        puzzle_input = load_input('test/test2_4.txt')
        assert part2(puzzle_input) == 5

    def test_2_5(self):
        puzzle_input = load_input('test/test2_5.txt')
        assert part2(puzzle_input) == 14
