# Load any required modules. Most commonly used:

import re
from itertools import combinations
import z3
import numpy as np
import scipy as sp

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
    print(model.eval(x), model.eval(y), model.eval(z))
    print(model.eval(vx), model.eval(vy), model.eval(vz))

    return result


def get_independent_hailstones(puzzle_input, n=3):
    """Get n independent hailstones, i.e. the curves
    of the stones are not parallel."""
    result = [puzzle_input[0]]
    curr_stone = 1
    while len(result) < n:
        # compare all stones in the result with the current stones
        # and check if their curves are not parallel
        # Parallel = all their v values are the same multiple of the
        # corresponding v value i.e. vx1 == n * vx2, vy1 == n * vy2 etc
        k = puzzle_input[curr_stone]
        parallel = False
        for h in result:
            if (h[3] / k[3]) == (h[4] / k[4]) == (h[5] / k[5]):
                parallel = True
                break
        if not parallel:
            result.append(k)
        curr_stone += 1

    return result


@aoc_timer
def part2_np_solve(puzzle_input):
    """Using 6 linear equations for the 6 variables (xr, yr, zr, vxr, vyr, vzr),
    solve the equations using np.linalg.solve."""
    # get 3 independent hailstones from the input
    stones = get_independent_hailstones(puzzle_input, 3)

    """
    We have 6 unknowns for the rock r:
    xr, yr, zr, vxr, vyr, vzr

    The x position of a hailstone at time t can be expressed as x = x1 + vx1 * t
    Similarly, the y position can be expressed as y = y1 + vx1 * t

    For the rock, similar calculation: x = xr + vxr * t, y = yr + vyr * t, z = zr + vzr * t

    The rock and a hailstone h1 are at the same position at the same time t if the 
    following equation is satisfied:
    x1 + vx1 * t = xr + vxr * t
    y1 + vy1 * t = yr + vyr * t
    z1 + vy1 * t = zr + vzr * t

    Rearrange to isolate t:
    t = (x1 - xr) / (vxr - vx1) = (y1 - yr) / (vyr - vy1)

    Rearrange these equations for x, y; x, z; y, z pairs gives 3 equations
    (x1 - xr) * (vyr - vy1) = (y1 - yr) * (vxr - vx1) for each of the pairs
    Rearrange into linear equations with the non-linear terms on the left:
    yr * vxr - xr * vyr = -vy1 * xr + vx1 * yr + vxr * y1 - vyr * x1 + vy1 * x1 - vx1 * y1

    The non-linear term on the left side is constant and the same for other hailstones h2 and h3,
    so set this to equal for another hailstone and group by the unknowns. Then do this for pairs
    x, y; x, z and y, z, and for hailstones h1 and h3. This yields 6 equations for 6 unknowns, so
    can be resolved using Gauss-Jordan matrix elimination etc.

    Formulas for hailstones 1 and 2:
    (vy2 - vy1) * xr + (vx1 - vx2) * yr + (y1 - y2) * vxr + (x2 - x1) * vyr = y1 * vx1 - x1 * vy1 + x2 * vy2 - y2 * vx2 
    (vz2 - vz1) * xr + (vx1 - vx2) * zr + (z1 - z2) * vxr + (x2 - x1) * vzr = z1 * vx1 - x1 * vz1 + x2 * vz2 - z2 * vx2 
    (vy2 - vy1) * zr + (vz1 - vz2) * yr + (y1 - y2) * vzr + (z2 - z1) * vyr = y1 * vz1 - z1 * vy1 + z2 * vy2 - y2 * vz2 
    Formulas for hailstones 1 and 3:
    (vy3 - vy1) * xr + (vx1 - vx3) * yr + (y1 - y3) * vxr + (x3 - x1) * vyr = y1 * vx1 - x1 * vy1 + x3 * vy3 - y3 * vx3 
    (vz3 - vz1) * xr + (vx1 - vx3) * zr + (z1 - z3) * vxr + (x3 - x1) * vzr = z1 * vx1 - x1 * vz1 + x3 * vz3 - z3 * vx3 
    (vy3 - vy1) * zr + (vz1 - vz3) * yr + (y1 - y3) * vzr + (z3 - z1) * vyr = y1 * vz1 - z1 * vy1 + z3 * vy3 - y3 * vz3 
    

    Use np.linalg.solve to solve equation: ax = b, where
    - a: N*N matrix of coefficients
    - b: N vector of dependent variables
    - x: N vector of variables to be solved for
    
    a (coefficient matrix) is in format [[xr, yr, zr, vxr, vyr, vzr], []]

    Unfortunately, due to the large numbers involved this is not precise and the
    values for xr, yr, and zr are slightly off the real values :(
    """
    a = []
    b = []
    for h, k in [[stones[0], stones[1]], [stones[0], stones[2]]]:
        # x, y
        a.append([k[4] - h[4], h[3] - k[3], 0, h[1] - k[1], k[0] - h[0], 0])
        # x, z
        a.append([k[5] - h[5], 0, h[3] - k[3], h[2] - k[2], 0, k[0] - h[0]])
        # y, z
        a.append([0, h[5] - k[5], k[4] - h[4], 0, k[2] - h[2], h[1] - k[1]])
        # x, y
        b.append(h[1] * h[3] - h[0] * h[4] + k[0] * k[4] - k[1] * k[3])
        # x, z
        b.append(h[2] * h[3] - h[0] * h[5] + k[0] * k[5] - k[2] * k[3])
        # y, z
        b.append(h[1] * h[5] - h[2] * h[4] + k[2] * k[4] - k[1] * k[5])

    a = np.array(a)
    b = np.array(b)

    x = sp.linalg.solve(a, b)
    print(x[0], x[1], x[2])
    print(x[3], x[4], x[5])
    print(np.round(x[0]), np.round(x[1]), np.round(x[2]))
    result = int(np.sum(x[:3]))
    # unfortunately, this is not fully correct for the large numbers
    # used here, the solve method does seem to make some floating point
    # rounding during the decomposition so the values are off by 3 in total :(

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

    # Solve part 2 using the equations and np.linalg.solve
    p2 = part2_np_solve(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 10:11 End: 12:24
# Part 2: Start: 13:32 End: 15:36

# Elapsed time to run part1: 0.04912 seconds.
# Part 1: 16939
# Elapsed time to run part2: 0.25026 seconds.
# Part 2: 931193307668256
