# Load any required modules. Most commonly used:

# import re
from collections import defaultdict
from utils.aoctools import aoc_timer


class Digi():
    def __init__(self, s) -> None:
        self.identity = None
        self.elements = set(list(s))

    def __len__(self):
        return len(self.elements)

    def __repr__(self) -> str:
        return f'[{self.identity}]: {self.elements}'


class DigiDisplay():

    def __init__(self, scrambled) -> None:
        self.confirmed_digits = {}
        self.unconfirmed_digits = []
        # self.assigned = {}
        self.reverse_digits = {}
        for s in scrambled:
            digi = Digi(s)
            if len(digi) == 2:
                self.confirmed_digits[1] = digi
                digi.identity = 1
            elif len(digi) == 4:
                self.confirmed_digits[4] = digi
                digi.identity = 4
            elif len(digi) == 3:
                self.confirmed_digits[7] = digi
                digi.identity = 7
            elif len(digi) == 7:
                self.confirmed_digits[8] = digi
                digi.identity = 8
            else:
                self.unconfirmed_digits.append(digi)

    def __repr__(self) -> str:
        return f'{self.confirmed_digits}'

    def solve(self):
        # find aa - difference between 1 and 7
        # aa = self.confirmed_digits[7].elements ^ self.confirmed_digits[1].elements
        # self.assigned['a'] = aa.pop()

        # find d, c and e from the 6 length elements
        # 6 does not contain both elements from 1
        length_six = [d for d in self.unconfirmed_digits if len(d) == 6]
        for d in length_six:
            if not all(x in d.elements for x in self.confirmed_digits[1].elements):
                self.confirmed_digits[6] = d
                d.identity = 6
                break
        self.unconfirmed_digits.remove(self.confirmed_digits[6])

        # find c - difference between 8 and 6
        # cc = self.confirmed_digits[8].elements ^ self.confirmed_digits[6].elements
        # self.assigned['c'] = cc.pop()

        # find 0 and d / 9 and e
        # d is not in 0 (remove 0 and 9 from 8 and use remainder) and in 4
        length_six = [d for d in self.unconfirmed_digits if len(d) == 6]
        for d in length_six:
            delta = (self.confirmed_digits[8].elements ^ d.elements).pop()
            if delta in self.confirmed_digits[4].elements:
                # self.assigned['d'] = delta
                self.confirmed_digits[0] = d
                self.unconfirmed_digits.remove(d)
                d.identity = 0
            else:
                # self.assigned['e'] = delta
                self.confirmed_digits[9] = d
                self.unconfirmed_digits.remove(d)
                d.identity = 9

        # find f - we know c so it is the other element in 1
        # ff = (self.confirmed_digits[1].elements ^
            #   set([self.assigned['c']])).pop()
        # self.assigned['f'] = ff

        # find 5 - the 5 digit number that differs only by one element from 6
        length_five = [d for d in self.unconfirmed_digits if len(d) == 5]
        for d in length_five:
            delta = (self.confirmed_digits[6].elements ^ d.elements)
            if len(delta) == 1:
                self.confirmed_digits[5] = d
                d.identity = 5
                self.unconfirmed_digits.remove(d)

        # find 3 - the 5 digit number that differs only by one element from 9
        # at the same time, the differing element is b
        length_five = [d for d in self.unconfirmed_digits if len(d) == 5]
        for d in length_five:
            delta = (self.confirmed_digits[9].elements ^ d.elements)
            if len(delta) == 1:
                self.confirmed_digits[3] = d
                d.identity = 3
                self.unconfirmed_digits.remove(d)
                # self.assigned['b'] = delta.pop()

        # 2 is the remaining 5 digit number
        self.confirmed_digits[2] = self.unconfirmed_digits[0]
        self.confirmed_digits[2].identity = 2
        self.unconfirmed_digits.remove(self.confirmed_digits[2])

        # g is the remaining unassigned segment
        # gg = (self.confirmed_digits[8].elements ^ set(self.assigned)).pop()
        # self.assigned['g'] = gg

        # print(self.assigned)
        # for k, v in self.confirmed_digits.items():
        #     print(k, v)
        # print(self.unconfirmed_digits)

        # create a reverse lookup dictionary so we can lookup the signals from the input
        for i in range(10):
            k = ''.join(sorted(self.confirmed_digits[i].elements))
            self.reverse_digits[k] = i


def load_input(f_name):
    """Loads the puzzle input from the specified file. 

    Specify the relative path if loading files from a subdirectory, 
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            a, b = line.strip().split(' | ')
            patterns = a.split()
            outputs = b.split()
            puzzle_input.append((patterns, outputs))

    return puzzle_input


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    c = defaultdict(int)
    for _, o in puzzle_input:
        for p in o:
            c[len(p)] += 1

    # length:digit: 2:1, 4:4, 3:7, 7:8
    result = c[2] + c[4] + c[3] + c[7]

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    result = 0
    for s, o in puzzle_input:
        digidisplay = DigiDisplay(s)
        digidisplay.solve()
        # now look up the resulting numbers
        decoded_value = ''
        for x in o:
            x = ''.join(sorted(x))
            decoded_value += str(digidisplay.reverse_digits[x])

        result += int(decoded_value)

    return result


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/08.txt')
    # puzzle_input = load_input('testinput/08_1_1.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 11:20 End: 11:53
# Part 2: Start:  End: 15:25
