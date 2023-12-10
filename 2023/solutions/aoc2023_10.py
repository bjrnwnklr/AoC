# Load any required modules. Most commonly used:

# import re
from collections import deque
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


def parse_grid(puzzle_input):
    """Parse the puzzle input into a 2d grid.

    Return
    - a 2d grid  - a dictionary with (r, c): pipe
    - the starting position marked by 'S'
    """
    grid = dict()
    for r, line in enumerate(puzzle_input):
        for c, ch in enumerate(line):
            grid[(r, c)] = ch
            if ch == "S":
                start = (r, c)

    return start, grid


MOVES_DIR = {
    # allowed moves up
    (-1, 0): {"|", "F", "7", "S"},
    # allowed moves down
    (1, 0): {"|", "J", "L", "S"},
    # allowed moves left
    (0, -1): {"-", "L", "F", "S"},
    # allowed moves right
    (0, 1): {"-", "J", "7", "S"},
}

MOVES_FROM = {
    "|": ((-1, 0), (1, 0)),
    "-": (
        (
            0,
            1,
        ),
        (0, -1),
    ),
    "L": ((-1, 0), (0, 1)),
    "J": ((-1, 0), (0, -1)),
    "7": ((1, 0), (0, -1)),
    "F": ((1, 0), (0, 1)),
    "S": ((-1, 0), (0, 1), (1, 0), (0, -1)),
    ".": ((-1, 0), (0, 1), (1, 0), (0, -1)),
}


def BFS(grid, start):
    """Run a Breadth First Search (BFS) on the complete pipe system,
    starting at S. Return the maximum number of steps found.
    And return the tiles contained in the loop.
    """
    seen = set()
    max_dist = 0
    q = deque([(start, 0)])
    while q:
        # get next node
        curr, steps = q.popleft()

        if curr in seen:
            continue

        seen.add(curr)
        # update maximum distance travelled
        max_dist = max(max_dist, steps)

        # find next steps and add to the queue
        for delta in MOVES_FROM[grid[curr]]:
            next_pos = (curr[0] + delta[0], curr[1] + delta[1])
            # check if the next position has a valid pipe to move to
            if (
                next_pos in grid
                and grid[next_pos] in MOVES_DIR[delta]
                and next_pos not in seen
            ):
                # add to queue
                q.append((next_pos, steps + 1))

    return max_dist, seen


resolution = {
    "|": [[".", "|", "."], [".", "|", "."], [".", "|", "."]],
    "-": [[".", ".", "."], ["-", "-", "-"], [".", ".", "."]],
    "F": [[".", ".", "."], [".", "F", "-"], [".", "|", "."]],
    "7": [[".", ".", "."], ["-", "7", "."], [".", "|", "."]],
    "J": [[".", "|", "."], ["-", "J", "."], [".", ".", "."]],
    "L": [[".", "|", "."], [".", "L", "-"], [".", ".", "."]],
    ".": [[".", ".", "."], [".", ".", "."], [".", ".", "."]],
}


def increase_grid(puzzle_input, factor):
    """Increase the resolution of the grid by factor provided.

    Returns a new grid, a dictionary of middle tiles and the new
    start position (middle of the new tile)."""
    grid = dict()
    # tiles is a dictionary of the middle cells of the new
    # enhanced resolution grid. These will be used to count
    # any cells that have been reached with the BFS and marked
    # as outer cells
    tiles = dict()
    for r, line in enumerate(puzzle_input):
        for c, ch in enumerate(line):
            rr = r * factor
            cc = c * factor
            if ch == "S":
                # found start tile, record start and replace with
                # appropriate grid
                start = (rr + 1, cc + 1)
                # replace with new til
                right = puzzle_input[r][c + 1] in MOVES_DIR[(0, 1)]
                left = puzzle_input[r][c - 1] in MOVES_DIR[(0, -1)]
                up = puzzle_input[r - 1][c] in MOVES_DIR[(-1, 0)]
                down = puzzle_input[r + 1][c] in MOVES_DIR[(1, 0)]
                if right and left:
                    ch = "-"
                elif right and up:
                    ch = "L"
                elif right and down:
                    ch = "F"
                elif up and down:
                    ch = "|"
                elif left and down:
                    ch = "7"
                elif left and up:
                    ch = "J"
                else:
                    raise ValueError("Unknown neighbors for S")

            if ch in resolution:
                # increase resolution
                for gr, row in enumerate(resolution[ch]):
                    for gc, col_char in enumerate(row):
                        grid[(gr + rr, gc + cc)] = col_char
                # store middle tile so we can count visited tiles
                # correctly
                tiles[(rr + 1, cc + 1)] = False

    return grid, tiles, start


def BFS_2(grid, loop, tiles, start):
    """Run a BFS on the outer tiles of the grid. Start should be
    in the upper left corner of the grid

    Return the number of tiles (middle tile of the
    enhanced grid) that can be reached this way.
    """
    seen = set()
    q = deque([(start, 0)])
    while q:
        # get next node
        curr, steps = q.popleft()

        if curr in seen:
            continue

        seen.add(curr)
        # Flip status of a tile if it is a middle tile we want
        # to count
        if curr in tiles:
            tiles[curr] = True

        # find trivial next steps (the ones we can reach directly) and add to the queue
        # including diagonal steps
        for delta in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            next_pos = (curr[0] + delta[0], curr[1] + delta[1])
            # check if the next position has a valid pipe to move to
            if next_pos in grid and next_pos not in loop and next_pos not in seen:
                # add to queue
                q.append((next_pos, steps + 1))

    return tiles


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    start, grid = parse_grid(puzzle_input)

    # build a BFS to explore the pipe system - flood fill
    # record the distance of each tile and then take the maximum
    # of the recorded distances
    result, _ = BFS(grid, start)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # increase resolution of the grid from 1x1 into 3x3
    # the middle of the tile is still the area that counts
    # if it can be reached and only if it is free and not part of
    # the loop
    grid, tiles, start = increase_grid(puzzle_input, 3)

    # build a BFS to explore the pipe system - flood fill
    # record the distance of each tile and then take the maximum
    # of the recorded distances
    _, loop = BFS(grid, start)

    # now run a second BFS that paints tiles that can be visited from
    # the outside. We start in the top left corner. Since we increase
    # the resolution, we don't need to add any outer rim around
    # the grid anymore, it is guaranteed to have free tiles around it
    outer_tiles = BFS_2(grid, loop, tiles, (0, 0))

    # count if inner tiles is:
    # outer_tiles == False - outer_tiles that are in loop
    inner_tiles = set(k for k in outer_tiles if not outer_tiles[k] and k not in loop)

    return len(inner_tiles)


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/10.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 10:57 End: 11:43
# Part 2: Start: 11:44  End: 16:13 (incl break)

# Elapsed time to run part1: 0.01391 seconds.
# Part 1: 6738
# Elapsed time to run part2: 0.20812 seconds.
# Part 2: 579
