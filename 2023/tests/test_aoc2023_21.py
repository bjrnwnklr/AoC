"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2023_21 import load_input, part1, part2, BFS, parse_grid


class Test_AOC2023_21:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition,
     put the example in a `test_n_n.txt` file in the `test` directory,
     and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_1(self):
        puzzle_input = load_input("testinput/21_1_1.txt")
        assert part1(puzzle_input, 6) == 16

    def test_2_1(self):
        puzzle_input = load_input("input/21.txt")
        rocks, start, width, height = parse_grid(puzzle_input)

        # 65 steps, even count
        steps = 65
        result = BFS(rocks, start, width, height, steps, even=True)
        print(f"Reachable in even {steps} steps from position: start {start}: {result}")
        assert result == 3768
        # 65 steps, odd count
        result = BFS(rocks, start, width, height, steps, even=False)
        print(f"Reachable in odd {steps} steps from position: start {start}: {result}")
        assert result == 3877

        # We establish that 131 steps, starting from the middle already
        # reaches all possible positions in the tile
        for n in range(1, 3):
            steps = n * 131
            result = BFS(rocks, start, width, height, steps, even=True)
            print(
                f"Reachable in even {steps} steps from position: start {start}: {result}"
            )
            assert result == 7688
            result = BFS(rocks, start, width, height, steps, even=False)
            print(
                f"Reachable in odd {steps} steps from position: start {start}: {result}"
            )
            assert result == 7656

        # from the corner, not every position is reachable in w+s (131 + 65) steps
        steps = 131 + 65
        start = (0, 0)
        result = BFS(rocks, start, width, height, steps, even=True)
        print(f"Reachable in even {steps} steps from position: start {start}: {result}")
        result = BFS(rocks, start, width, height, steps, even=False)
        print(f"Reachable in odd {steps} steps from position: start {start}: {result}")
