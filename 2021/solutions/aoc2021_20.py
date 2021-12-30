# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from itertools import product
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.

    Convert # into 1 and . into 0s.
    """
    with open(f_name, 'r') as f:
        algo, bottom = f.read().split('\n\n')
        algo = [1 if x == '#' else 0 for x in algo.strip()]
        image = set()
        for r, line in enumerate(bottom.split('\n')):
            for c, x in enumerate(line.strip()):
                if x == '#':
                    image.add((r, c))

    return (algo, image)


def print_image(image: set[tuple[int]], padding: int = 5):
    """Output a pixel representation of the image."""

    min_r, max_r, min_c, max_c = img_dimensions(image)
    print()
    for r in range(min_r, max_r + 1):
        line = ''
        for c in range(min_c, max_c + 1):
            line += '#' if (r, c) in image else '.'
        print(line)
    print()


def neighbors(r: int, c: int) -> list[tuple[int]]:
    """Calculate the resulting pixel score of the 9 neighboring pixels in (r, c) notation.
    Includes the input (r, c) pixel.
    """
    offsets = [-1, 0, 1]
    return [
        (r + dr, c + dc)
        for dr, dc in product(offsets, repeat=2)
    ]


def img_dimensions(image: set[tuple[int]]) -> tuple[tuple[int]]:
    """Calculate the dimensions of the visible image by taking the
    space occupied by "lit" pixels (== 1 value).

    Adds padding of 1 pixel to each side.
    """
    padding = 0
    min_r = min(image, key=lambda x: x[0])[0] - padding
    max_r = max(image, key=lambda x: x[0])[0] + padding
    min_c = min(image, key=lambda x: x[1])[1] - padding
    max_c = max(image, key=lambda x: x[1])[1] + padding

    return (min_r, max_r, min_c, max_c)


def default_pixel(algo):
    """Returns the default infinity pixel value for even cycles (default pixel dark) and
    for uneven cycles (default pixel lit).
    """
    odd = str(algo[int(
        ''.join(str(algo[0]) * 9),
        base=2
    )])
    even = str(algo[0])

    cycle = 1
    while True:
        yield even if cycle % 2 == 0 else odd
        cycle += 1


def lit_pixels(image: set[tuple[int]]) -> int:
    """Calculate the number of lit pixels in an image."""
    return len(image)


@aoc_timer
def part1(puzzle_input, cycles=2):
    """Solve part 1. Return the required output value."""

    algo, image = puzzle_input
    min_r, max_r, min_c, max_c = img_dimensions(image)

    # alternate the default pixel in infinity between the algo[0] (for odd cycles)
    # and what algo[9 * algo[0]] yields - which is what any infinite pixels get flipped to
    # on the next cycle.
    infinity_generator = default_pixel(algo)
    for i in range(1, cycles + 1):
        # get next infinity character
        infpix = next(infinity_generator)
        # apply image algorithm
        new_image = set()
        for r in range(min_r - 1, max_r + 2):
            for c in range(min_c - 1, max_c + 2):
                s = ''
                for nr, nc in neighbors(r, c):
                    if min_r <= nr <= max_r and min_c <= nc <= max_c:
                        s += '1' if (nr, nc) in image else '0'
                    else:
                        s += infpix
                i = int(s, base=2)
                if algo[i] == 1:
                    new_image.add((r, c))

        # extend frame by one on each side as image grows by 1 on each side during
        # each enhancement
        min_r -= 1
        max_r += 1
        min_c -= 1
        max_c += 1

        image = new_image

    return lit_pixels(image)


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/20.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part1(puzzle_input, 50)
    print(f'Part 2: {p2}')

# Part 1: Start: 17:23 End: 19:30
# Part 2: Start: 19:31 End: 19:41

# Elapsed time to run part1: 0.10244 seconds.
# Part 1: 5400
# Elapsed time to run part1: 5.54760 seconds.
# Part 2: 18989
