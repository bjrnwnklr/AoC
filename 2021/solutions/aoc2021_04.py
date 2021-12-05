# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer
import numpy as np


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `test/test1_1.txt`.
    """
    with open(f_name, 'r') as f:
        # first line is bingo numbers
        bingo_numbers = list(map(int, f.readline().strip().split(',')))

        # parse the bingo boards by splitting remaining input by two line breaks
        boards_raw = f.read().split('\n\n')

        boards = [
            Board(b) for b in boards_raw
        ]

    return bingo_numbers, boards


class Board:
    def __init__(self, b) -> None:
        self.marked = np.zeros((5, 5), dtype=bool)
        grid = [
            list(map(int, row.split()))
            for row in b.strip().split('\n')
        ]
        self.board = np.array(grid)
        self.won = False

    def __str__(self) -> str:
        out = 'Board: \n'
        out += self.board.__str__()
        out += '\nMarked: \n'
        out += self.marked.__str__()
        return out

    def mark(self, n):
        """Mark a number on the board, then check if the board is complete"""
        mask = np.isin(self.board, [n])
        self.marked[mask] = True
        return self.bingo()

    def bingo(self):
        """Return true if either a row or a column of the board is filled."""
        rows = self.marked.all(axis=1)
        row_bingo = rows.any()

        cols = self.marked.all(axis=0)
        col_bingo = cols.any()

        if col_bingo or row_bingo:
            self.won = True

        return self.won

    def score(self):
        """Calculate the score of the board - sum of all unmarked numbers"""
        s = self.board[~self.marked].sum()
        return s


@aoc_timer
def part1(bingo_numbers, boards):
    """Solve part 1. Return the required output value."""

    # go through numbers and mark each number on the board
    for n in bingo_numbers:
        for board in boards:
            bingo_won = board.mark(n)
            if bingo_won:
                # we have a bingo!
                result = board.score() * n
                break
        if bingo_won:
            break

    return result


@aoc_timer
def part2(bingo_numbers, boards):
    """Solve part 2. Return the required output value."""

    # how many boards are remaining?
    remaining_boards = len(boards)

    # go through numbers and mark each number on the board
    for n in bingo_numbers:
        for board in boards:
            if not board.won:
                bingo_won = board.mark(n)
                if bingo_won:
                    # we have a bingo, mark the board as won and reduce number of remaining boards
                    remaining_boards -= 1
                    # if this was the last board, we have our winner
                    if remaining_boards == 0:
                        result = board.score() * n

    return result


if __name__ == '__main__':
    # read the puzzle input
    bingo_numbers, boards = load_input('input/04.txt')

    # Solve part 1 and print the answer
    p1 = part1(bingo_numbers, boards)
    print(f'Part 1: {p1}')

    bingo_numbers, boards = load_input('input/04.txt')
    # Solve part 2 and print the answer
    p2 = part2(bingo_numbers, boards)
    print(f'Part 2: {p2}')

# Part 1: Start: 17:58 End: 15:13 (next day - ca 1 hour)
# Part 2: Start: 15:20 End: 15:27
