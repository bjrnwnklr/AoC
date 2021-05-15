def neighbors_on(coord, current_state):
    on_count = 0
    for rd in (-1, 0, 1):
        r = coord[0] + rd
        for cd in (-1, 0, 1):
            c = coord[1] + cd
            if (r, c) != coord and (r, c) in current_state:
                on_count += 1

    return on_count


def turns_on(coord, current_state):
    n_on = neighbors_on(coord, current_state)
    if coord in current_state and n_on in (2, 3):
        return True
    elif coord not in current_state and n_on == 3:
        return True
    else:
        return False


def turn_corners_on(current_state):
    for coord in [(0, 0), (0, dims[1] - 1), (dims[0] - 1, 0), (dims[0] - 1, dims[1] - 1)]:
        current_state.add(coord)


def print_grid(current_state):
    for r in range(dims[0]):
        line = ''
        for c in range(dims[1]):
            line += '#' if (r, c) in current_state else '.'

        print(line)


if __name__ == '__main__':

    # steps = 5
    steps = 100

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        lines = f.readlines()

    lights_on = set()
    dims = (len(lines), len(lines[0].strip()))

    for r, line in enumerate(lines):
        for c, light in enumerate(line.strip()):
            if light == '#':
                lights_on.add((r, c))

    turn_corners_on(lights_on)

    for s in range(steps):
        next_state = set()
        for r in range(dims[0]):
            for c in range(dims[1]):
                if turns_on((r, c), lights_on):
                    next_state.add((r, c))

        lights_on = next_state
        turn_corners_on(lights_on)

    print(len(lights_on))

    # Part 1: 821
    # Part 2: 886
