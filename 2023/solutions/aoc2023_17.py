# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
from heapq import heappop, heappush
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
            puzzle_input.append([int(n) for n in list(line.strip())])

    # Extract ints from the input
    #
    # signed ints
    # regex = re.compile(r"(-?\d+)")
    #
    # unsigned ints
    # regex = re.compile(r"(\d+)")
    #
    # with open(f_name, "r") as f:
    #     puzzle_input = []
    #     for line in f.readlines():
    #         matches = regex.findall(line.strip())
    #         if matches:
    #             puzzle_input.append(list(map(int, matches)))

    return puzzle_input


# 0: right, 1: down, 2: left, 3, up
# moves are: left, straight, right
DIRS = {
    0: [(-1, 0), (0, 1), (1, 0)],
    1: [(0, 1), (1, 0), (0, -1)],
    2: [(1, 0), (0, -1), (-1, 0)],
    3: [(0, -1), (-1, 0), (0, 1)],
}


def dijkstra(grid, start, end):
    """Run Dijkstra's search algorithm to find the lowest heat dissipation
    going through the grid.

    Constraints:
    - can only go maximum of 3 consecutive steps in a straight line
      before turning left or right
    - can only go left, right or straight but not back."""
    seen = set()
    # dimensions of the grid
    height = len(grid)
    width = len(grid[0])
    distance_to = defaultdict(lambda: 1e9)
    # q = [(heat, r, c, steps, dir)]
    q = [(0, start[0], start[1], 0, 0)]
    while q:
        # get next element from priority queue - the one with
        # the lowest heat loss
        curr_heat, curr_r, curr_c, curr_steps, curr_dir = heappop(q)

        # check if this state has already been seen
        if (curr_heat, curr_r, curr_c, curr_steps, curr_dir) in seen:
            continue

        # check if we have reached the end
        if (curr_r, curr_c) == end:
            return curr_heat

        # else, add to seen
        seen.add((curr_heat, curr_r, curr_c, curr_steps, curr_dir))

        # get possible moves and add to priority queue
        # DIRS is the possible moves (left, straight, right).
        # We start at -1 to enumerate to calculate the new direction
        # This allows us to change direction by adding the new direction
        # and taking modulo 4 (e.g. left turn: (0 + -1) % 4 = 3)
        for i, (dr, dc) in enumerate(DIRS[curr_dir], start=-1):
            rr = curr_r + dr
            cc = curr_c + dc
            if 0 <= rr < height and 0 <= cc < width:
                # get heat loss from next cell
                next_heat = grid[rr][cc]
                # check if the next cell can be reached with lower heat loss
                # than before
                hl = curr_heat + next_heat
                next_dir = (curr_dir + i) % 4
                # check if we can move straight
                if i == 0:
                    if (
                        curr_steps < 3
                        and hl < distance_to[(rr, cc, curr_steps + 1, next_dir)]
                    ):
                        # move straight
                        heappush(
                            q,
                            (
                                (
                                    hl,
                                    rr,
                                    cc,
                                    curr_steps + 1,
                                    next_dir,
                                )
                            ),
                        )
                        distance_to[(rr, cc, curr_steps + 1, next_dir)] = hl
                else:
                    if hl < distance_to[(rr, cc, 1, next_dir)]:
                        # move left or right
                        heappush(
                            q,
                            (
                                hl,
                                rr,
                                cc,
                                1,
                                next_dir,
                            ),
                        )
                        distance_to[(rr, cc, 1, next_dir)] = hl

    # if we get to here, we never found the end
    return -1


def dijkstra_2(grid, start, end):
    """Run Dijkstra's search algorithm to find the lowest heat dissipation
    going through the grid.

    Constraints:
    - can only turn or stop after going straight for 4
    - has to turn after 10 straight
    - can only go left, right or straight but not back."""
    seen = set()
    # dimensions of the grid
    height = len(grid)
    width = len(grid[0])
    distance_to = defaultdict(lambda: 1e9)
    # q = [(heat, r, c, steps, dir)]
    q = [(0, start[0], start[1], 0, 0)]
    while q:
        # get next element from priority queue - the one with
        # the lowest heat loss
        curr_heat, curr_r, curr_c, curr_steps, curr_dir = heappop(q)

        # check if this state has already been seen
        if (curr_heat, curr_r, curr_c, curr_steps, curr_dir) in seen:
            continue

        # check if we have reached the end
        if (curr_r, curr_c) == end and curr_steps >= 4:
            return curr_heat

        # else, add to seen
        seen.add((curr_heat, curr_r, curr_c, curr_steps, curr_dir))

        # get possible moves and add to priority queue
        # DIRS is the possible moves (left, straight, right).
        # We start at -1 to enumerate to calculate the new direction
        # This allows us to change direction by adding the new direction
        # and taking modulo 4 (e.g. left turn: (0 + -1) % 4 = 3)
        for i, (dr, dc) in enumerate(DIRS[curr_dir], start=-1):
            rr = curr_r + dr
            cc = curr_c + dc
            if 0 <= rr < height and 0 <= cc < width:
                # get heat loss from next cell
                next_heat = grid[rr][cc]
                # check if the next cell can be reached with lower heat loss
                # than before
                hl = curr_heat + next_heat
                next_dir = (curr_dir + i) % 4
                # check if we can move straight
                if i == 0:
                    if (
                        # need to turn after maximum of 10 consecutive straight steps
                        curr_steps < 10
                        and hl < distance_to[(rr, cc, curr_steps + 1, next_dir)]
                    ):
                        # move straight
                        heappush(
                            q,
                            (
                                (
                                    hl,
                                    rr,
                                    cc,
                                    curr_steps + 1,
                                    next_dir,
                                )
                            ),
                        )
                        distance_to[(rr, cc, curr_steps + 1, next_dir)] = hl
                else:
                    if curr_steps >= 4 and hl < distance_to[(rr, cc, 1, next_dir)]:
                        # move left or right
                        heappush(
                            q,
                            (
                                hl,
                                rr,
                                cc,
                                1,
                                next_dir,
                            ),
                        )
                        distance_to[(rr, cc, 1, next_dir)] = hl

    # if we get to here, we never found the end
    return -1


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    start = (0, 0)
    end = (len(puzzle_input) - 1, len(puzzle_input[0]) - 1)
    result = dijkstra(puzzle_input, start, end)

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    start = (0, 0)
    end = (len(puzzle_input) - 1, len(puzzle_input[0]) - 1)
    result = dijkstra_2(puzzle_input, start, end)

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/17.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 9:28 End: 10:55
# Part 2: Start: 10:56 End:

# Elapsed time to run part1: 0.98373 seconds.
# Part 1: 956
# Elapsed time to run part2: 3.48901 seconds.
# Part 2: 1106
