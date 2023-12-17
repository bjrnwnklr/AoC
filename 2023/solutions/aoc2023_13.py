# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
import hashlib
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = f.read()
    return puzzle_input


def hash_rows(lines):
    """Return a dictionary of row: hashvalue
    This can be used to compare if lines are identical.
    Uses MD5 to calculate the hash value."""
    d = dict()
    for r in range(len(lines)):
        d[r] = hashlib.md5(
            "".join(lines[r][c] for c in range(len(lines[0]))).encode()
        ).hexdigest()
    return d


def hash_cols(lines):
    """Return a dictionary of col: hashvalue
    This can be used to compare if columns are identical.
    Uses MD5 to calculate the hash value."""
    d = dict()
    for c in range(len(lines[0])):
        d[c] = hashlib.md5(
            "".join(lines[r][c] for r in range(len(lines))).encode()
        ).hexdigest()
    return d


def find_pairs(d: dict) -> list[tuple[int, int]]:
    """Return a list of row or column indexes that match.
    d is a dictionary of row/col index: hash."""
    m = max(d.keys())
    pairs = []
    for i in range(0, m + 1):
        for j in range(i + 1, m + 1):
            if d[i] == d[j]:
                pairs.append((i, j))
    return pairs


def is_mirror(pairs, highest):
    """Check if the pairs represent a mirror.
    To be a mirror:
    - pairs with increasing spread have to match
    - one of the matching rows / columns has to be
      at the end of the grid (first or last row or column)

    'highest' is the last line (row or column) of the pairs.

    Returns a list of the row or column where the reflection starts,
    or an empty list if no reflection."""
    # determine spread between each pair and select the pair that
    # has spread 1
    result = []
    starting_pairs = []
    for a, b in pairs:
        if b - a == 1:
            starting_pairs.append((a, b))

    if starting_pairs:
        # if any starting pairs have been found
        # iterate through the outward spreading pairs
        # and update the result if we find contiuous
        # outward spreading pairs until we either hit 0
        # or the highest index (i.e. reach the end of the
        # grid on either side)
        for a, b in starting_pairs:
            i = 1
            mirrors = True
            while i <= min(a, highest - b):
                if (a - i, b + i) in pairs:
                    # found a matching pair
                    i += 1
                else:
                    mirrors = False
                    break

            # if we get to here, evaluate if we found a matching mirror
            if mirrors:
                result.append(a)

    return result


def get_mirror_result(lines):
    """Generate the result of the provided mirror
    Rows get multiplied by 100 and columns return the number
    of columns to the left"""
    # generate hashes for each row and column
    # plus highest row and column index
    row_hashes = hash_rows(lines)
    highest_row = max(row_hashes)
    col_hashes = hash_cols(lines)
    highest_col = max(col_hashes)

    # check if any rows are matching
    # and find if any perfect mirror matching found in rows
    row_pairs = find_pairs(row_hashes)
    row_mirror_line = is_mirror(row_pairs, highest_row)

    col_pairs = find_pairs(col_hashes)
    col_mirror_line = is_mirror(col_pairs, highest_col)

    return row_mirror_line, col_mirror_line


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    result = 0
    # split input into individual sections
    for image in puzzle_input.split("\n\n"):
        lines = [[x for x in line] for line in image.strip().split("\n")]
        row_mirror_line, col_mirror_line = get_mirror_result(lines)
        if not row_mirror_line and not col_mirror_line:
            raise ValueError(f"No mirror line found: {image}")
        elif len(row_mirror_line) > 0:
            result += (row_mirror_line[0] + 1) * 100
        elif len(col_mirror_line) > 0:
            result += col_mirror_line[0] + 1

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    result = 0
    # split input into individual sections
    for image in puzzle_input.split("\n\n"):
        lines = [[x for x in line] for line in image.strip().split("\n")]
        # get original results
        orig_row_mirror_line, orig_col_mirror_line = get_mirror_result(lines)

        # iterate through rows and columns and change one cell,
        # then test if we found a mirror that is different to the one before
        found = False
        for r in range(len(lines)):
            for c in range(len(lines[0])):
                lines[r][c] = "." if lines[r][c] == "#" else "#"
                # process the new image
                row_mirror_line, col_mirror_line = get_mirror_result(lines)
                # check what we found
                # if there is at least one entry in the row mirror list,
                # go through one by one
                # if it is either a new entry because there was no original row mirror,
                # or if it is a different value - we then found a new entry.
                if len(row_mirror_line) > 0:
                    for row in row_mirror_line:
                        if (
                            len(orig_row_mirror_line) == 0
                            or row != orig_row_mirror_line[0]
                        ):
                            # found a new row mirror line, so let's take this
                            result += (row + 1) * 100
                            found = True
                            break
                if len(col_mirror_line) > 0:
                    for col in col_mirror_line:
                        if (
                            len(orig_col_mirror_line) == 0
                            or col != orig_col_mirror_line[0]
                        ):
                            # found a new column mirror line, so let's take this
                            result += col + 1
                            found = True
                            break
                # flip back to old value if we can't find anything, then proceed
                lines[r][c] = "." if lines[r][c] == "#" else "#"
                # multiple breaks required here to stop processing multiple new
                # mirrors (found one example that had multiple that could be flipped)
                if found:
                    break

            if found:
                break

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/13.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 10:29 End: 11:27
# Part 2: Start: 11:29 End: 14:32 (had to rewrite part 2 completely since i accidentally restored
# an old version before commiting :( )

# Elapsed time to run part1: 0.00494 seconds.
# Part 1: 30535
# Elapsed time to run part2: 0.33867 seconds.
# Part 2: 30844
