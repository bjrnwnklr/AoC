from aoc2021_02 import load_input, part1, part2


class Test202102:

    def test_1_1(self):
        puzzle_input = load_input('test/test1_1.txt')
        assert part1(puzzle_input) == 12

    def test_2_1(self):
        puzzle_input = load_input('test/test2_1.txt')
        assert part2(puzzle_input) == 'fgij'
