def load_input(f_name):
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(int(line.strip()))
    return puzzle_input


def part1(puzzle_input):
    return sum(puzzle_input)


def part2(puzzle_input):
    seen = set()
    freq = 0
    pos = 0
    while freq not in seen:
        seen.add(freq)
        freq += puzzle_input[pos]
        pos = (pos + 1) % len(puzzle_input)
    return freq


if __name__ == '__main__':
    puzzle_input = load_input('input.txt')

    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')
