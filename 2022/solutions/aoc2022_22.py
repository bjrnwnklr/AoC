# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
from dataclasses import dataclass

from utils.aoctools import aoc_timer


@dataclass
class Position:
    row: int
    col: int
    facing: int


# turn clockwise or anti-clockwise
turns = {"R": 1, "L": -1}
# move right, down, left, up
dirs = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
# to draw on the map
pointer = {0: ">", 1: "v", 2: "<", 3: "^"}
# side length, won't work for the example
l = 50


def which_side(pos):
    """Determine the side of the cube:
        1   2
        3
    4   5
    6

    l is the side length of the cube.
    """
    r = pos.row
    c = pos.col
    if 0 * l <= r < 1 * l and 1 * l <= c < 2 * l:
        return 1
    elif 0 * l <= r < 1 * l and 2 * l <= c < 3 * l:
        return 2
    elif 1 * l <= r < 2 * l and 1 * l <= c < 2 * l:
        return 3
    elif 2 * l <= r < 3 * l and 0 * l <= c < 1 * l:
        return 4
    elif 2 * l <= r < 3 * l and 1 * l <= c < 2 * l:
        return 5
    elif 3 * l <= r < 4 * l and 0 * l <= c < 1 * l:
        return 6


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        raw_map, instructions = f.read().rstrip().split("\n\n")

    return raw_map, instructions


def parse_map(raw_map):
    """Parse the raw map into a grid, which is a defaultdict that only includes
    entries for walkable spaces and walls."""
    # grid returns space for any coordinates not in the map
    grid = defaultdict(lambda: " ")
    for r, row in enumerate(raw_map.split("\n")):
        for c, col in enumerate(list(row)):
            grid[(r, c)] = col

    return grid


def parse_instructions(instructions):
    """Parse the instructions and return a list of numbers and left/right
    movements."""
    num = "0"
    result = []
    q = list(instructions)
    while q:
        i = q.pop(0)
        if i in ["L", "R"]:
            # add up numbers from previous collection
            n = int(num)
            num = "0"
            result.append(n)
            result.append(i)
        else:
            num += i
    # if there is anything left in num, write it out
    if num != "0":
        n = int(num)
        result.append(n)

    return result


def next_pos(pos):
    """Calculate the next position based on current direction."""
    rr, cc = pos.row + dirs[pos.facing][0], pos.col + dirs[pos.facing][1]
    return rr, cc


def wrap(pos, grid):
    """Calculate new wrapped position."""
    # depending on which direction player is facing, find the min or max
    # on the other side of the grid that is not a blank (can be a wall or
    # walkable space)
    good_space = [".", "#"]
    match pos.facing:
        case 0:
            # facing right, wrap around to left side
            # min of current row
            pos.col = min(
                c for r, c in grid.keys() if r == pos.row and grid[(r, c)] in good_space
            )
        case 1:
            # facing down, wrap around to top side
            # min of current col
            pos.row = min(
                r for r, c in grid.keys() if c == pos.col and grid[(r, c)] in good_space
            )
        case 2:
            # facing left, wrap around to right side
            # max of current row
            pos.col = max(
                c for r, c in grid.keys() if r == pos.row and grid[(r, c)] in good_space
            )
        case 3:
            # facing up, wrap around to bottom side
            # max of current col
            pos.row = max(
                r for r, c in grid.keys() if c == pos.col and grid[(r, c)] in good_space
            )

    return pos.row, pos.col


def wrap_cube(pos, grid):
    """Hard coded wrapping around the cube.
    Changes both the row/col and the facing value of the
    provided position.
    """
    # determine which side we are on
    cube = which_side(pos)
    # based on side of cube and which direction we are
    # facing, calculate the new row / col and the direction
    new_pos = Position(0, 0, 0)
    match cube, pos.facing:
        case 1, 3:
            # on side 1, facing up
            # we end up on 6, facing right
            new_pos.facing = 0
            new_pos.row = pos.col + 2 * l
            new_pos.col = 0
        case 1, 2:
            # on side 1 facing left
            # we end up side 4, facing right
            # also coordinates reverse (top goes to bottom)
            new_pos.facing = 0
            new_pos.row = (3 * l) - 1 - pos.row
            new_pos.col = 0
        case 2, 3:
            # on side 2, facing up
            # we end up on 6, facing up
            new_pos.facing = 3
            new_pos.row = pos.row + 4 * l - 1
            new_pos.col = pos.col - 2 * l
        case 2, 0:
            # on side 2, facing right
            # we end up on 5, facing left
            new_pos.facing = 2
            new_pos.row = (3 * l) - 1 - pos.row
            new_pos.col = 2 * l - 1
        case 2, 1:
            # on side 2, facing down
            # we end up on 3, facing left
            new_pos.facing = 2
            new_pos.row = pos.col - l
            new_pos.col = (2 * l) - 1
        case 3, 2:
            # on side 3, facing left
            # we end up on 4, facing down
            new_pos.facing = 1
            new_pos.row = 2 * l
            new_pos.col = pos.row - l
        case 3, 0:
            # on side 3, facing right
            # we end up on 2, facing up
            new_pos.facing = 3
            new_pos.row = l - 1
            new_pos.col = pos.row + l
        case 4, 3:
            # on side 4, facing up
            # we end up on 3, facing right
            new_pos.facing = 0
            new_pos.row = pos.col + l
            new_pos.col = l
        case 4, 2:
            # on side 4, facing left
            # we end up on 1, facing right
            new_pos.facing = 0
            new_pos.row = (3 * l) - 1 - pos.row
            new_pos.col = l
        case 5, 0:
            # on side 5, facing right
            # we end up on 2, facing left
            new_pos.facing = 2
            new_pos.row = (3 * l) - 1 - pos.row
            new_pos.col = (3 * l) - 1
        case 5, 1:
            # on side 5, facing down
            # we end up on 6, facing left
            new_pos.facing = 2
            new_pos.row = pos.col + 2 * l
            new_pos.col = l - 1
        case 6, 2:
            # on side 6, facing left
            # we end up on 1, facing down
            new_pos.facing = 1
            new_pos.row = 0
            new_pos.col = pos.row - 2 * l
        case 6, 1:
            # on side 6, facing down
            # we end up on 2, facing down
            new_pos.facing = 1
            new_pos.row = 0
            new_pos.col = pos.col + 2 * l
        case 6, 0:
            # on side 6, facing right
            # we end up on 5, facing up
            new_pos.facing = 3
            new_pos.row = 3 * l - 1
            new_pos.col = pos.row - 2 * l
        case _:
            # we found a case that isn't defined
            # raise an exception
            raise ValueError(
                f"wrap_cube case not implemented: {cube=}, {pos.facing=}. {pos=}"
            )

    return new_pos


def draw_map(pos, grid):
    """Draw an arrow onto the map at the current position."""
    grid[(pos.row, pos.col)] = pointer[pos.facing]


@aoc_timer
def part1(raw_map, instructions):
    """Solve part 1. Return the required output value.
    Rows start from 1 at the top and count downward; columns start from 1 at the
    left and count rightward. (In the above example, row 1, column 1 refers to
    the empty space with no tile on it in the top-left corner.) Facing is 0 for
    right (>), 1 for down (v), 2 for left (<), and 3 for up (^).

    The final password is the sum of 1000 times the row, 4 times the column, and
    the facing."""

    # parse the map into a grid
    grid = parse_map(raw_map)
    # create a copy of the grid
    # draw = parse_map(raw_map)

    # determine starting position, which is the lowest column
    # in row 0 that has a '.'.
    start_col = min(c for r, c in grid.keys() if r == 0 and grid[(r, c)] == ".")
    player = Position(0, start_col, 0)
    # print(f"Starting at {player}")
    # draw starting pos
    # draw_map(player, draw)

    # parse instructions
    inst = parse_instructions(instructions)

    # walk the grid
    for instruction in inst:
        if instruction in turns:
            # player turns clockwise or anti-clockwise
            player.facing = (player.facing + turns[instruction]) % 4
            # draw_map(player, draw)
        else:
            for _ in range(instruction):
                # check next grid cell in current direction
                rr, cc = next_pos(player)
                next_g = grid[(rr, cc)]
                match next_g:
                    case "#":
                        # wall, process next instruction
                        break
                    case " ":
                        # empty space, wrap around
                        # check if next position is not a wall as well
                        rw, cw = wrap(Position(rr, cc, player.facing), grid)
                        next_gw = grid[(rw, cw)]
                        if next_gw == "#":
                            # hit a wall, player stays
                            break
                        else:
                            # player moves to new wrapped location
                            player.row, player.col = rw, cw
                            # draw_map(player, draw)
                    case ".":
                        # walkable space, player moves to new location
                        player.row, player.col = rr, cc
                        # draw_map(player, draw)

    # finished walking?
    # calculate score of current position (add +1 to row and col)
    score = 1000 * (player.row + 1) + 4 * (player.col + 1) + player.facing
    # print(f"Finished, {player=}, {score=}")

    # dump out the instructions and map
    # with open("2022_22_instructions.txt", "w") as f:
    #     for i in inst:
    #         f.write(str(i) + "\n")
    # with open("2022_22_map.txt", "w") as f:
    #     max_row = max(r for r, c in draw.keys())
    #     max_col = max(c for r, c in draw.keys())
    #     for row in range(max_row):
    #         f.write("".join(draw[(row, col)] for col in range(max_col)) + "\n")

    return score


@aoc_timer
def part2(raw_map, instructions):
    """Solve part 2. Return the required output value.
    Rows start from 1 at the top and count downward; columns start from 1 at the
    left and count rightward. (In the above example, row 1, column 1 refers to
    the empty space with no tile on it in the top-left corner.) Facing is 0 for
    right (>), 1 for down (v), 2 for left (<), and 3 for up (^).

    The final password is the sum of 1000 times the row, 4 times the column, and
    the facing."""

    # parse the map into a grid
    grid = parse_map(raw_map)
    # create a copy of the grid
    # draw = parse_map(raw_map)

    # determine starting position, which is the lowest column
    # in row 0 that has a '.'.
    start_col = min(c for r, c in grid.keys() if r == 0 and grid[(r, c)] == ".")
    player = Position(0, start_col, 0)
    # print(f"Starting at {player}")
    # draw starting pos
    # draw_map(player, draw)

    # parse instructions
    inst = parse_instructions(instructions)

    # walk the grid
    for instruction in inst:
        # print(f"Instruction: {instruction}, {player=}")
        if instruction in turns:
            # player turns clockwise or anti-clockwise
            # print(f"Player turns from {player.facing} to ...")
            player.facing = (player.facing + turns[instruction]) % 4
            # print(f"\t to {player.facing}")
            # draw_map(player, draw)
        else:
            for _ in range(instruction):
                # check next grid cell in current direction
                rr, cc = next_pos(player)
                next_g = grid[(rr, cc)]
                match next_g:
                    case "#":
                        # wall, process next instruction
                        # print(f"Wall at {rr}, {cc}")
                        break
                    case " ":
                        # empty space, wrap around
                        # check if next position is not a wall as well
                        # print(f"Empty space, testing wrap around...")
                        new_pos = wrap_cube(player, grid)
                        # print(f"\t ... wrap to {new_pos}")
                        next_gw = grid[(new_pos.row, new_pos.col)]
                        if next_gw == "#":
                            # hit a wall, player stays
                            # print(f"\t ... which is a wall. Not moving.")
                            break
                        else:
                            # player moves to new wrapped location
                            player.row, player.col, player.facing = (
                                new_pos.row,
                                new_pos.col,
                                new_pos.facing,
                            )
                            # print(f"\t ... which is free, moving to {player}")
                            # draw_map(player, draw)
                    case ".":
                        # walkable space, player moves to new location
                        player.row, player.col = rr, cc
                        # print(f"Walkable space, moving to {player}")
                        # draw_map(player, draw)

    # finished walking?
    # calculate score of current position (add +1 to row and col)
    score = 1000 * (player.row + 1) + 4 * (player.col + 1) + player.facing
    # print(f"Finished, {player=}, {score=}")

    # dump out the instructions and map
    # with open("2022_22_instructions.txt", "w") as f:
    #     for i in inst:
    #         f.write(str(i) + "\n")
    # with open("2022_22_map.txt", "w") as f:
    #     max_row = max(r for r, c in draw.keys())
    #     max_col = max(c for r, c in draw.keys())
    #     for row in range(max_row):
    #         f.write("".join(draw[(row, col)] for col in range(max_col)) + "\n")

    return score


if __name__ == "__main__":
    # read the puzzle input
    raw_map, instructions = load_input("input/22.txt")
    # raw_map, instructions = load_input("input/22_5_steps.txt")

    # Solve part 1 and print the answer
    p1 = part1(raw_map, instructions)
    print(f"Part 1: {p1}")

    raw_map, instructions = load_input("input/22.txt")
    # Solve part 2 and print the answer
    p2 = part2(raw_map, instructions)
    print(f"Part 2: {p2}")

# Part 1: Start: 16:44 End: 19:00
# Part 2: Start: 16:08 End: 13:30 next day

# Elapsed time to run part1: 0.19385 seconds.
# Part 1: 197160
# Elapsed time to run part2: 0.01226 seconds.
# Part 2: 145065
