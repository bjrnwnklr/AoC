# Load any required modules. Most commonly used:

import re
from collections import defaultdict, Counter


def load_input(f_name):
    """Loads the puzzle input from the specified file. Specify the relative path 
    if loading files from a subdirectory, e.g. for loading test inputs, specify
    `test/test1_1.txt`.

    Depending on the puzzle, change how the lines in the file are parsed, what format
    the extracted values have etc.

    Args:
        f_name (String): File name of the input file.

    Returns:
        List: A list of the inputs read in.
    """
    with open(f_name, 'r') as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return sorted(puzzle_input)


def parse_guards(puzzle_input):
    # parse through each line and find events depending on text in line
    regex = re.compile(r'(\d+)')
    # guards is a dict of guards with a list of minutes they were asleep
    # dict is per guard
    # list consists of the minutes the guard was asleep
    guards = defaultdict(list)
    for line in puzzle_input:
        # find all numbers in the line and put in a list
        numbers = list(map(int, regex.findall(line)))
        if 'Guard' in line:
            # the only thing we need to do when we find a guard line is note down which guard
            # has now taken the shift.
            # guard id is #5 in the list
            guard = numbers[5]
        elif 'asleep' in line:
            # note down the time the guard falls asleep - we will mark the time once he wakes up
            # only the minute part (#4 in the list) is relevant
            asleep = numbers[4]
        elif 'wakes' in line:
            # mark all minutes the guard sleeps in a dictionary entry of the guard
            # note the minute when the guard wakes up
            awake = numbers[4]
            for minute in range(asleep, awake):
                guards[guard].append(minute)

    return guards


def part1(puzzle_input):
    """Solve part 1. Return the required output value.

    Args:
        puzzle_input (List): Typically a list of the input values from the input.txt puzzle input.

    Returns:
        Depends...: Typically an Integer value, but often also a String - this can be used on adventofcode 
        as the answer to the puzzle.
    """
    guards = parse_guards(puzzle_input)

    # find the guard who slept the most minutes
    max_minutes = 0
    chosen_guard = -1
    for guard in guards:
        minutes_asleep = len(guards[guard])
        if minutes_asleep > max_minutes:
            max_minutes = minutes_asleep
            chosen_guard = guard

    # find the minute with the most sleep for the chosen guard
    sleepy_guard_minutes = guards[chosen_guard]
    # most_common returns a list of tuples (minute, count) so we need the first element of the list
    # and from that the first element (minute) of the tuple
    c = Counter(sleepy_guard_minutes)
    chosen_minute = c.most_common(1)[0][0]
    # return (ID of guard chosen) * (minute chosen)
    return chosen_guard * chosen_minute


def part2(puzzle_input):
    """Solve part 2. Return the required output value.

    Args:
        puzzle_input (List): Typically a list of the input values from the input.txt puzzle input.

    Returns:
        Depends...: Typically an Integer value, but often also a String - this can be used on adventofcode 
        as the answer to the puzzle.
    """
    guards = parse_guards(puzzle_input)

    # for each guard, find the minute they are most asleep at, then compare across all guards
    # and take the max of that
    max_minute_per_guard = dict()
    for guard in guards:
        max_minute_per_guard[guard] = Counter(guards[guard]).most_common(1)[0]

    # now find the guard with the highest minute count
    # use the second element of the tuple for each guard entry (minute, number of times asleep)
    # to find the max
    chosen_guard = max(max_minute_per_guard,
                       key=lambda x: max_minute_per_guard[x][1])

    return chosen_guard * max_minute_per_guard[chosen_guard][0]


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

    # Part 1: 38813
    # Part 2: 141071 (2879 * 49)
