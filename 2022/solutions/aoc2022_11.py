# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        raw_monkeys = f.read().split('\n\n')

        puzzle_input = {}
        for monkey in raw_monkeys:
            for line in monkey.split('\n'):
                match line.strip().split():
                    case ['Monkey', d]:
                        number = int(d[:-1])
                    case ['Starting', _, *d]:
                        items = [int(x.strip(',')) for x in d]
                    case ['Operation:', *_, 'old']:
                        operation = '^'
                        factor = 0
                    case ['Operation:', *_, op, f]:
                        operation = op
                        factor = int(f)
                    case ['Test:', *_, d]:
                        divisible = int(d)
                    case ['If', 'true:', *_, m]:
                        test_t = int(m)
                    case ['If', 'false:', *_, m]:
                        test_f = int(m)
            
            puzzle_input[number] = Monkey(
                number,
                items,
                operation,
                factor,
                divisible,
                test_t,
                test_f
            )
            logger.debug(f'Created new monkey: {puzzle_input[number]}')

    return puzzle_input


@dataclass
class Monkey:
    number: int
    items: list
    operation: str
    factor: int
    divisible: int
    test_t: int
    test_f: int
    inspected: int = 0


def inspect(monkey, monkeys):
    """Inspect an item by executing operation on value"""
    logger.debug(f"Monkey {monkey.number}:")
    if monkey.items:
        item = monkey.items.pop(0)

        logger.debug(f"\tMonkey inspects an item with a worry level of {item}.")
        match monkey.operation:
            case "*":
                item *= monkey.factor
                logger.debug(f"\t\tWorry level is multiplied by {monkey.factor} to {item}.")
            case "+":
                item += monkey.factor
                logger.debug(f"\t\tWorry level increases by {monkey.factor} to {item}.")
            case '^':
                item *= item 
                logger.debug(f"\t\tWorry level is multiplied by self to {item}.")

        item = item // 3
        logger.debug(
            f"\t\tMonkey gets bored with item. Worry level is divided by 3 to {item}."
        )

        if item % monkey.divisible == 0:
            logger.debug(f"\t\tCurrent worry level is divisible by {monkey.divisible}.")
            other_monkey = monkey.test_t
        else:
            logger.debug(f"\t\tCurrent worry level is not divisible by {monkey.divisible}.")
            other_monkey = monkey.test_f

        monkeys[other_monkey].items.append(item)
        logger.debug(f"\tItem with worry level {item} is thrown to monkey {other_monkey}.")

        # increase monkey inspect count
        monkey.inspected += 1
    else:
        logger.debug(f'\tMonkey {monkey.number} has no items.')

def inspect_2(monkey, monkeys):
    """Inspect an item by executing operation on value"""
    logger.debug(f"Monkey {monkey.number}:")
    if monkey.items:
        item = monkey.items.pop(0)

        logger.debug(f"\tMonkey inspects an item with a worry level of {item}.")
        match monkey.operation:
            case "*":
                item *= monkey.factor
                logger.debug(f"\t\tWorry level is multiplied by {monkey.factor} to {item}.")
            case "+":
                item += monkey.factor
                logger.debug(f"\t\tWorry level increases by {monkey.factor} to {item}.")
            case '^':
                item *= item 
                logger.debug(f"\t\tWorry level is multiplied by self to {item}.")

        if item % monkey.divisible == 0:
            logger.debug(f"\t\tCurrent worry level is divisible by {monkey.divisible}.")
            other_monkey = monkey.test_t
            item = monkeys[other_monkey].divisible
        else:
            logger.debug(f"\t\tCurrent worry level is not divisible by {monkey.divisible}.")
            other_monkey = monkey.test_f
            item = item % monkeys[other_monkey].divisible

        # for part 2, take the item % other_monkey.divisible as that 
        # produces the same result (divisibles are all primes, likely some
        # number theory theorem with modulo arithmetic)      
        logger.debug(f'\tAdjusting item level down to {item}.')

        monkeys[other_monkey].items.append(item)
        logger.debug(f"\tItem with worry level {item} is thrown to monkey {other_monkey}.")

        # increase monkey inspect count
        monkey.inspected += 1
    else:
        logger.debug(f'\tMonkey {monkey.number} has no items.')


# @aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value.
    Figure out which monkeys to chase by counting how many items
    they inspect over 20 rounds.

    What is the level of monkey business after 20 rounds
    of stuff-slinging simian shenanigans?
    - inspect: apply formula to worry level
    - divide by three, rounded down
    - test
    - pass on based on test rules
    """

    for i in range(20):
        for j in range(len(puzzle_input)):
            monkey = puzzle_input[j]
            while monkey.items:
                inspect(monkey, puzzle_input)

        logger.debug(f'After round {i}, the monkeys are holding items:')
        for m in puzzle_input.values():
            logging.debug(f'Monkey {m.number}: {m.items}')

    # calculate two most active monkeys
    m1, m2 = sorted(puzzle_input, key=lambda x: puzzle_input[x].inspected, reverse=True)[:2]

    return puzzle_input[m1].inspected * puzzle_input[m2].inspected


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    for i in range(10_000):
        for j in range(len(puzzle_input)):
            monkey = puzzle_input[j]
            while monkey.items:
                inspect_2(monkey, puzzle_input)

        if (i + 1) % 1000 == 0:
            logger.info(f'-- After round {i + 1} --')
            for m in puzzle_input:
                monkey = puzzle_input[m]
                logger.info(f'Monkey {monkey.number} inspected items {monkey.inspected} times')

    # calculate two most active monkeys
    m1, m2 = sorted(puzzle_input, key=lambda x: puzzle_input[x].inspected, reverse=True)[:2]

    return puzzle_input[m1].inspected * puzzle_input[m2].inspected


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/11.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    puzzle_input = load_input("input/11.txt")
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 17:06 End: 18:16
# Part 2: Start: 18:17 End:
