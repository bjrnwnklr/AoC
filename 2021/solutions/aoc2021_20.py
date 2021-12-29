# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
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
        image = {}
        for r, line in enumerate(bottom.split('\n')):
            for c, x in enumerate(line.strip()):
                image[(r, c)] = 1 if x == '#' else 0

    return (algo, image)


def print_image(image: defaultdict[tuple[int], int]):
    """Output a pixel representation of the image."""

    min_r, max_r, min_c, max_c = img_dimensions(image)
    print()
    for r in range(min_r, max_r + 1):
        line = ''
        for c in range(min_c, max_c + 1):
            line += '#' if image.get((r, c), 0) == 1 else '.'
        print(line)
    print()


def neighbors(r: int, c: int) -> list[tuple[int]]:
    """Calculate 9 neighboring pixels in (r, c) notation.
    Includes the input (r, c) pixel.
    """
    offsets = [-1, 0, 1]
    return [
        (r + dr, c + dc)
        for dr, dc in product(offsets, repeat=2)
    ]


def img_dimensions(image: defaultdict[tuple[int], int]) -> list[tuple[int]]:
    """Calculate the dimensions of the visible image by taking the
    space occupied by "lit" pixels (== 1 value).

    Adds padding of 1 pixel to each side.
    """
    padding = 1
    lit_pixel_coords = [x for x in image if image[x] == 1]
    min_r = min(lit_pixel_coords, key=lambda x: x[0])[0] - padding
    max_r = max(lit_pixel_coords, key=lambda x: x[0])[0] + padding
    min_c = min(lit_pixel_coords, key=lambda x: x[1])[1] - padding
    max_c = max(lit_pixel_coords, key=lambda x: x[1])[1] + padding

    return [min_r, max_r, min_c, max_c]


def apply_algo(image: defaultdict[tuple[int], int], algo: list[int], cycle: int) -> defaultdict[tuple[int], int]:
    """Apply image enhancement algorithm to the provided image once.

    Depending how many cycles are being done of the algorithm, the default pixel value
    switches from dark (on even number of cycles, starting with 0) to light (on uneven
    number of cycles, starting with 1).
    """
    # determine image dimensions - need to consider frame of 1 pixel
    # outside of the widest pixels
    min_r, max_r, min_c, max_c = img_dimensions(image)
    # alternate the default pixel in infinity between the algo[0] (for odd cycles)
    # and what algo[9 * algo[0]] yields - which is what any infinite pixels get flipped to
    # on the next cycle.
    even = algo[int(
                ''.join(str(algo[0]) * 9),
                base=2
                )]
    odd = algo[0]

    # on even number of cycles, default pixel is 0, on others it is 1
    new_image = {}
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            i = int(
                ''.join(str(image.get((nr, nc), default_pixel(cycle, even, odd)))
                        for nr, nc in neighbors(r, c)),
                base=2
            )
            new_image[(r, c)] = algo[i]

    return new_image


def default_pixel(cycle, even, odd):
    """Returns the default pixel value - 0 for even cycles (default pixel dark),
    1 for uneven cycles (default pixel lit).
    """
    return even if cycle % 2 == 0 else odd


def lit_pixels(image: defaultdict[tuple[int], int]) -> int:
    """Calculate the number of lit pixels in an image."""
    return sum(image[coord] for coord in image)


@aoc_timer
def part1(puzzle_input, cycles=2):
    """Solve part 1. Return the required output value."""

    algo, image = puzzle_input

    # print(f'Original image: {lit_pixels(image)} pixels lit.')
    # print(f'Dimensions: {img_dimensions(image)}')

    for i in range(cycles):
        image = apply_algo(image, algo, i)
        # print(f'Algo pass {i}: {lit_pixels(image)} pixels lit.')
        # print(f'Dimensions: {img_dimensions(image)}')

    return lit_pixels(image)


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


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
