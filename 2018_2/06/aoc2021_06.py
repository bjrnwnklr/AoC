# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
import math


def load_input(f_name):
    """Loads the puzzle input from the specified file. Specify the relative path 
    if loading files from a subdirectory, e.g. for loading test inputs, specify
    `test/test1_1.txt`.

    Depending on the puzzle, change how the lines in the file are parsed, what format
    the extracted values have etc.

    Args:
        f_name (String): File name of the input file.

    Returns:
        List: A list of the inputs read in.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        # CHANGE HERE: depending on the input file, change how the lines are processed and what
        # happens with the extracted values, e.g. convert to Integer.
        for line in f.readlines():
            puzzle_input.append(list(map(int, line.strip().split(','))))

    return puzzle_input


def distance(a, b):
    """Calculates the manhattan distance between two points.

    Args:
        a (tuple): (x, y) coordinates of point a
        b (tuple): (x, y) coordinates of point b

    Returns:
        Int: manhattan distance between point a and point b
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def nearest_planet(c, planets):
    """Returns the id (index in list of planets) of the closest planet to (x, y) coordinate `c`.
    If more than one planet are closest, returns -1.

    Args:
        c (tuple): (x, y) coordinate of the point to check.
        planets (List): List of planets in (x, y) form.

    Returns:
        int: Integer index of the closest planet. -1 if more than one planet is at closest distance.
    """
    dist = [distance(c, p) for p in planets]
    min_dist = min(dist)

    # check if distance occurs multiple times
    if dist.count(min_dist) > 1:
        result = -1
    else:
        result = dist.index(min_dist)

    return result


def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    Args:
        puzzle_input (List): Typically a list of the input values from the input.txt puzzle input.

    Returns:
        Depends...: Typically an Integer value, but often also a String - this can be used on adventofcode 
        as the answer to the puzzle.
    """
    # determine outer boundaries of the grid - min / max coordinates of the grid
    # extend the grid by one point to each side
    min_x = min(x for x, _ in puzzle_input) - 1
    min_y = min(y for _, y in puzzle_input) - 1
    max_x = max(x for x, _ in puzzle_input) + 1
    max_y = max(y for _, y in puzzle_input) + 1

    # for each point in the grid, calculate the nearest planet (measure Manhattan Distance to each planet)
    # if > 1 nearest, mark as not counting
    # Put this into a function
    grid = {
        (x, y): nearest_planet((x, y), puzzle_input)
        for y in range(min_y, max_y + 1)
        for x in range(min_x, max_x + 1)
    }
    # identify infinity - any points on the outer rim nearest to a planet identify that planet as reaching
    # into infinity
    outer_rim = (
        set(grid[x, y] for x in range(min_x, max_x + 1)
            for y in [min_y, max_y])
        | set(grid[x, y] for y in range(min_y, max_y + 1) for x in [min_x, max_x])
    )

    candidate_planets = [
        p for p in range(len(puzzle_input))
        if p not in outer_rim
    ]

    # take non-infinity planets and count their areas
    # Take maximum area and that's our planet
    all_grid_points = list(grid.values())
    return max(all_grid_points.count(p) for p in candidate_planets)


def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    Args:
        puzzle_input (List): Typically a list of the input values from the input.txt puzzle input.

    Returns:
        Depends...: Typically an Integer value, but often also a String - this can be used on adventofcode 
        as the answer to the puzzle.
    """
    # Add code here

    return 1


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')
