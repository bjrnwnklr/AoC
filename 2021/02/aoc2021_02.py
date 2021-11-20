from collections import Counter


def load_input(f_name):
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())
    return puzzle_input


def part1(puzzle_input):
    counts = {2: 0, 3: 0}

    for word in puzzle_input:
        c = Counter(word)
        for n in counts:
            if n in c.values():
                counts[n] += 1

    return counts[2] * counts[3]


def diff_pos(a, b):
    return sum(
        1 if a[i] != b[i] else 0
        for i in range(len(a))
    )


def part2(puzzle_input):
    for box_a in puzzle_input:
        for box_b in puzzle_input:
            if box_a != box_b and diff_pos(box_a, box_b) == 1:
                return ''.join(c for c in box_a if c in box_b)

    return ''


if __name__ == '__main__':
    puzzle_input = load_input('input.txt')

    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')
