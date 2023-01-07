# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer
import logging
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = []
        line = f.readline()
        puzzle_input = list(line.strip())

    return puzzle_input


class Shape:

    # shapes are described by the relative coordinates of the filled parts of the shape
    # to an anchor (e.g. bottom left corner)
    # (e.g. the plus) in (r, c) notation

    rocks = {
        0: [(0, 0), (0, 1), (0, 2), (0, 3)],  # -
        1: [(0, 1), (-1, 0), (-1, 1), (-1, 2), (-2, 1)],  # +
        2: [(0, 0), (0, 1), (0, 2), (-1, 2), (-2, 2)],  # reverse L
        3: [(0, 0), (-1, 0), (-2, 0), (-3, 0)],  # I
        4: [(0, 0), (0, 1), (-1, 0), (-1, 1)],  # cube
    }
    directions = {">": (0, 1), "<": (0, -1), "v": (1, 0)}

    def __init__(self, id, last_row) -> None:
        # pick the shape based on id
        self.coords = self.rocks[id % 5][:]
        # move to starting position
        for i in range(len(self.coords)):
            self.coords[i] = (self.coords[i][0] + last_row - 4, self.coords[i][1] + 3)

        # logging.debug(f"Created shape: {self.coords}")

    def move_coords(self, direction):
        """Provide a list of updated coordinates after a move left,
        right or downward."""
        dd = self.directions[direction]
        return [(block[0] + dd[0], block[1] + dd[1]) for block in self.coords]

    def move(self, direction):
        """Move the shape in the specified direction."""
        self.coords = self.move_coords(direction)
        # logging.debug(f"Moved shape in direction {direction}: {self.coords}")


class Room:

    # Represents the narrow tall room

    # The walls / floor are set up like this:
    # - bottom left corner: (0, 0)
    # - left wall: (x, 0) with x < 0
    # - right wall: (x, 8) with x < 0
    # - the first free row in between is (-1, 1) - (-1, 7)

    def __init__(self) -> None:
        self.grid = set()

    def is_collision(self, coords) -> bool:
        """Checks if a provided shape hits a wall, floor or other
        stopped rock.

        `coords`: list of coordinates of the shape
        """
        # check for collision
        for block in coords:
            if (
                block in self.grid  # hit a stopped rock
                or block[1] == 0  # hit left wall
                or block[1] == 8  # hit right wall
                or block[0] == 0  # hit floor
            ):
                return True

        return False

    def move(self, shape: Shape, direction: str) -> bool:
        """Moves a shape
        - first in the indicated direction '<' or '>'
        - then downwards 'v'

        Returns True if the downward move was successful (i.e. False if it hit
        a stopped rock or the floor on the downward movement).
        """
        # sideways move
        potential_coords = shape.move_coords(direction)
        if not self.is_collision(potential_coords):
            shape.move(direction)
        # downwards move
        potential_coords = shape.move_coords("v")
        if not self.is_collision(potential_coords):
            shape.move("v")
            # if successful, return True
            return True
        else:
            # hit the floor or came to rest on other rock
            # freeze the rock and return False
            for c in shape.coords:
                self.grid.add(c)
            return False

    def height(self):
        """Returns the height of the tower of rocks in the room."""
        if self.grid:
            return min(self.grid, key=lambda x: x[0])[0]
        else:
            return 0


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    How many units tall will the tower of rocks be after 2022 rocks
    have stopped falling?
    """
    rocks = 0
    total_jet_movements = len(puzzle_input)
    jet = 0
    room = Room()

    while rocks < 2022:
        # logging.debug(f"New rock: {rocks}")
        # put next shape in at the height of the tower
        s = Shape(rocks, room.height())
        while True:
            move_successful = room.move(s, puzzle_input[jet % total_jet_movements])
            jet += 1

            if not move_successful:
                # logging.debug(f"Rock stopped {rocks}, height: {room.height()}")
                rocks += 1
                break

    return -room.height()


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    How tall will the tower be after 1000000000000 rocks have stopped?

    Assumed that there is a cyclic repetition somewhere in the movements
    of jet and blocks. Probably related to having 5 rocks and the length of the
    jet movements.

    Test case: heights repeat with the following frequency:

    15 (first 15 are unique)
    after that, every 35 rocks have the same height sequence (53 total)


    """
    rocks = 0
    total_jet_movements = len(puzzle_input)
    jet = 0
    room = Room()
    heights = []

    while rocks < 10_000:
        # put next shape in at the height of the tower
        s = Shape(rocks, room.height())
        while True:
            move_successful = room.move(s, puzzle_input[jet % total_jet_movements])
            jet += 1

            if not move_successful:
                heights.append(room.height())
                rocks += 1
                break

    # Find the cyclic pattern with the following approach:
    # - pick a starting point, e.g. rock 1000
    # - check height differences for 3 cycles of length n
    #   and see if they have the same height difference.
    #   Start with a reasonable n, e.g. 30
    # - Once the length of the cycle is found, find the starting point.
    #   Do a binary search down from starting point and check if the
    #   same height difference from n is found
    df = pd.DataFrame(heights, columns=["height"])
    starting_point = 1000
    n = 30
    while True:
        indices = [starting_point + n * i for i in range(4)]
        df_diff = df.iloc[indices]["height"].diff().iloc[1:]
        if (df_diff == df_diff.iloc[0]).all():
            break

        n += 1

    # cycles = number of rocks that form a cycle
    # height = height of the stack of rocks in one cycle
    cycles = n
    height = int(-df_diff.iloc[0])

    # now binary search for the starting point where the cycle starts
    low = 0
    high = 1000
    while (high - low) > 1:
        mid = low + (high - low) // 2
        print(f"Search in {low=} {high=}, {mid=}")
        indices = [mid + cycles * i for i in range(4)]
        df_diff = df.iloc[indices]["height"].diff().iloc[1:]
        if (df_diff == df_diff.iloc[0]).all():
            # too high, go with lower half interval
            high = mid
        else:
            low = mid

    # low = last rock that is not part of the cycle
    # mid = first rock where the cycle starts

    # calculate the full height of rocks:
    # height of lower part until cycle starts
    # + height of cycle * number of cycles in 1_000_000.... - mid
    # + height of remaining rocks in cycle (as the last cycle will not be a full cycle)
    low_part = -df.iloc[low]["height"]
    mid_part = ((1_000_000_000_000 - mid) // cycles) * height
    remaining_rocks = (1_000_000_000_000 - mid) % cycles
    upper_part = -df.iloc[remaining_rocks + low]["height"] + df.iloc[low]["height"]

    return low_part + mid_part + upper_part


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/17.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start:  End:
# Part 2: Start:  End:
