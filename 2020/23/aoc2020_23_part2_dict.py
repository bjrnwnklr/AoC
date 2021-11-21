
def simulate(next_elements, start_cup, rounds):
    current_cup = start_cup
    max_cup = max(next_elements)
    for cycles in range(rounds):

        # if cycles % 1_000 == 0:
        #     print(f'{cycles=}')

        # pick three cups
        c1 = next_elements[current_cup]
        c2 = next_elements[c1]
        c3 = next_elements[c2]

        # find destination cup
        dest_cup = current_cup
        while dest_cup in {current_cup, c1, c2, c3}:
            dest_cup -= 1
            if dest_cup == 0:
                dest_cup = max_cup

        # place the cup clockwise next to the destination cup
        # 1) link the current cup to the next of c3
        next_elements[current_cup] = next_elements[c3]
        # 2) link c3 to the next of destination cup
        next_elements[c3] = next_elements[dest_cup]
        # 3) link destination cup to c1
        next_elements[dest_cup] = c1

        # pick next current cup
        current_cup = next_elements[current_cup]


def create_dict(cups):
    return {
        n: cups[(i + 1) % len(cups)]
        for i, n in enumerate(cups)
    }


if __name__ == '__main__':
    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        cups_initial = [int(x) for x in list(f.read().strip())]

    # part 1
    start_cup = cups_initial[0]
    next_elements = create_dict(cups_initial)

    simulate(next_elements, start_cup, 100)
    part1 = ''
    i = 1
    while (n := next_elements[i]) != 1:
        part1 += str(n)
        i = n

    print(f'Part 1: {part1}')

    # part 2
    start_cup = cups_initial[0]
    next_elements = create_dict(cups_initial + list(range(max(cups_initial) + 1, 1_000_000 + 1)))

    simulate(next_elements, start_cup, 10_000_000)
    n1 = next_elements[1]
    n2 = next_elements[n1]

    part2 = n1 * n2
    print(f'Part 2: {part2} = {n1} * {n2}')

# Part 1: 34952786
# Part 2: 505334281774 = 595814 * 848141
