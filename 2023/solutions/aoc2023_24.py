# Load any required modules. Most commonly used:

import re
from itertools import combinations
import z3

# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # signed ints
    regex = re.compile(r"(-?\d+)")
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            matches = regex.findall(line.strip())
            if matches:
                puzzle_input.append(list(map(int, matches)))

    return puzzle_input


def fy(px, py, vx, vy, x):
    return py + vy * ((x - px) / vx)


def fx(px1, py1, vx1, vy1, px2, py2, vx2, vy2):
    """This finds the x coordinate where both intersect.

    The equation was painstakingly solved on paper :)
    """
    # check if they are parallel and return None in case both curves
    # run parallel to each other - avoids division by zero
    if (vx1 / vx2) == (vy1 / vy2):
        return None
    else:
        return (vx1 * vx2 * (py1 - py2) + vx1 * vy2 * px2 - vx2 * vy1 * px1) / (
            vx1 * vy2 - vx2 * vy1
        )


def ft(px, vx, x):
    return (x - px) / vx


def get_intersection(px1, py1, vx1, vy1, px2, py2, vx2, vy2):
    """Calculate the point where the lines expressed by
    f(x) = px + vx * x and f(y) = py + vy * y intersect
    for values px1, px2, vx1 etc

    Checks if lines are parallel ((vx1 / vx2) == (vy1 / vy2))
    and returns None for both values if they are parallel -
    otherwise formula for x would produce a division by zero.
    """
    x_intersect = fx(px1, py1, vx1, vy1, px2, py2, vx2, vy2)
    if x_intersect:
        y_intersect = fy(px1, py1, vx1, vy1, x_intersect)
        return x_intersect, y_intersect
    else:
        return None, None


@aoc_timer
def part1(puzzle_input, intersect_min, intersect_max):
    """Solve part 1. Return the required output value."""
    hailstones = puzzle_input
    # x and y can be expressed as linear equation:
    # f(t) = px + vx * t
    # These parametric equations can be converted into rectangular equations
    # by eliminating the t parameter - solve for t in one equation and substitute
    # in the other.
    # This results in y = f(px, py, vx, vy, x) = py + vy * ((x - px) / vx)
    # The intersection between two such equations can be found by
    # 1) solving for x when equating both - this gives the x coordinate where they intersect
    # 2) inserting the found x value (x intercept) into the rectangular equation,
    #    which yields the y value
    result = 0
    for h1, h2 in combinations(hailstones, 2):
        x_intersection, y_intersection = get_intersection(
            h1[0], h1[1], h1[3], h1[4], h2[0], h2[1], h2[3], h2[4]
        )
        if (
            x_intersection
            and y_intersection
            and intersect_min <= x_intersection <= intersect_max
            and intersect_min <= y_intersection <= intersect_max
        ):
            # check if any of the intersections happened in the past - plug x and y intercepts into the original
            # formula f(p, v, x) = (x - p) / v and see if it is a negative value - happened in the past then!
            if all(
                ft(p, v, intersection) >= 0
                for p, v, intersection in [
                    (h1[0], h1[3], x_intersection),
                    (h2[0], h2[3], x_intersection),
                ]
            ):
                result += 1

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    # using z3 solver to solvep
    # using solution from jonathanpaulson:
    # https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/24.py
    stones = puzzle_input
    # add rock variables to resolve
    # we want to solve for x, y and z
    x = z3.Real("x")
    y = z3.Real("y")
    z = z3.Real("z")
    vx = z3.Real("vx")
    vy = z3.Real("vy")
    vz = z3.Real("vz")

    # add times for each hailstone as a variables
    times = [z3.Real(f"t{i}") for i in range(len(stones))]
    # create solver
    solver = z3.Solver()

    # add constraints for each hailstone
    # constraints need to satisfy the condition that the hailstone and the rock
    # need to be at the same x, y and z coordinate at a given time
    # this can be expressed as
    #  position of rock - position of hailstone == 0
    #  x + vx * t - (hx + vhx * t)
    for i in range(len(stones)):
        solver.add(x + times[i] * vx - (stones[i][0] + times[i] * stones[i][3]) == 0)
        solver.add(y + times[i] * vy - (stones[i][1] + times[i] * stones[i][4]) == 0)
        solver.add(z + times[i] * vz - (stones[i][2] + times[i] * stones[i][5]) == 0)
    # check consistency of model
    _ = solver.check()
    model = solver.model()
    # run model and return the sum of x y and z that satisfy all the constraints
    result = model.eval(x + y + z)

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/24.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input, 200_000_000_000_000, 400_000_000_000_000)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 10:11 End: 12:24
# Part 2: Start: 13:32 End: 15:36

# Elapsed time to run part1: 0.04912 seconds.
# Part 1: 16939
# Elapsed time to run part2: 0.25026 seconds.
# Part 2: 931193307668256
