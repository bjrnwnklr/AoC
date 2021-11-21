class Cup:
    def __init__(self, label, next=None):
        self.label = label
        self.next = next

    def __repr__(self):
        return f'Node({self.label})->{self.next.label}'


class CrabCupsGame:
    def __init__(self, initial_cups_config):
        self.max_label = max(initial_cups_config)
        # create initial cup instances without any links. We will add links in a second pass.
        self.cup_register = {c: Cup(c) for c in initial_cups_config}
        # do a second pass and link the cup instances to their follower.
        # Break around at the end of the list to link it back to the first one.
        for i, c in enumerate(initial_cups_config):
            if i == self.max_label - 1:
                n = initial_cups_config[0]
            else:
                n = initial_cups_config[i + 1]
            self.cup_register[c].next = self.cup_register[n]
        # set the current cup
        self.current_cup = self.cup_register[initial_cups_config[0]]

    def __len__(self):
        return len(self.cup_register)

    def __repr__(self):
        return f'CrabCupGame({self.__len__()})'

    def play(self, cycles):
        for _ in range(cycles):
            # pick up 3 cups
            c1 = self.current_cup.next
            c2 = c1.next
            c3 = c2.next

            # pick destination cup
            d_label = self.current_cup.label
            while d_label in {self.current_cup.label, c1.label, c2.label, c3.label}:
                d_label -= 1
                if d_label == 0:
                    d_label = self.max_label
            destination_cup = self.cup_register[d_label]

            # place the 3 cups behind the destination cup and re-link the current cup
            self.current_cup.next = c3.next
            c3.next = destination_cup.next
            destination_cup.next = c1

            # rotate the current cup
            self.current_cup = self.current_cup.next

    def part1(self):
        p1_output_cup = self.cup_register[1].next
        part1_result = ''
        while p1_output_cup.label != 1:
            part1_result += str(p1_output_cup.label)
            p1_output_cup = p1_output_cup.next
        return part1_result

    def part2(self):
        c1 = self.cup_register[1].next
        c2 = c1.next
        return c1.label, c2.label


if __name__ == '__main__':
    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        initial_cups_config = [int(x) for x in list(f.read().strip())]

    # part 1
    ccc = CrabCupsGame(initial_cups_config)
    print(ccc)
    ccc.play(100)
    print(f'Part 1: {ccc.part1()}')

    # part 2
    max_cup = max(initial_cups_config)
    ccc = CrabCupsGame(initial_cups_config + list(range(max_cup + 1, 1_000_001)))
    print(ccc)
    ccc.play(10_000_000)
    c1, c2 = ccc.part2()
    print(f'Part 2: {c1 * c2} = {c1} * {c2}')


# Part 1: 34952786
# Part 2: 505334281774 = 595814 * 848141
