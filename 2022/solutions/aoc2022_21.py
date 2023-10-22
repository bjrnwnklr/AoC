# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    # Specify the relative path if loading files from a subdirectory,
    # e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    #"""
    # # return input as list of text lines
    with open(f_name, "r") as f:
        monkeys_op = {}  # monkeys with formula
        monkeys_n = {}  # monkeys with numbers
        for line in f.readlines():
            left, right = line.strip().split(":")
            if any(x in right for x in ["+", "/", "*", "-"]):
                # found a monkey with arithmetic
                a, op, b = right.strip().split(" ")
                monkeys_op[left] = (a, op, b)
            else:
                # found a monkey with a number
                monkeys_n[left] = int(right)

    return monkeys_op, monkeys_n


def calc(a, op, b):
    """Calculate the value of two ints a and b with the operator op."""
    match op:
        case "+":
            return a + b
        case "*":
            return a * b
        case "/":
            return a // b
        case "-":
            return a - b


@aoc_timer
def part1(monkeys_op, monkeys_n):
    """Solve part 1. Return the required output value."""
    # print(monkeys_op, monkeys_n)
    # process numbers first and replace any occurrence in formulas
    # check if a formula is all numbers, then calculate and add to numbers queue to process
    q = list(monkeys_n.keys())
    while q:
        n_key = q.pop()
        # print(f"Looking where to replace {n_key}")
        # check if we found root
        if n_key == "root":
            break
        to_remove = []
        for o in monkeys_op:
            if n_key in monkeys_op[o]:
                # found a monkey that has the number key in its formula
                # replace the monkey name with the number
                monkeys_op[o] = tuple(
                    x if x != n_key else monkeys_n[n_key] for x in monkeys_op[o]
                )
                # print(f"Replaced {n_key} in {o}: {monkeys_op[o]}")
                # now check if we found a formula that has two ints in it
                # we can then calculate the result
                if sum(isinstance(x, int) for x in monkeys_op[o]) == 2:
                    # print(f"Found a completed formula! {o}: {monkeys_op[o]}")
                    # add to numbers monkey list
                    monkeys_n[o] = calc(*monkeys_op[o])
                    q.append(o)
                    # add to removal list
                    to_remove.append(o)

        # remove any processed numbers from the remaining formula monkeys
        for removal in to_remove:
            del monkeys_op[removal]
        # print what we currently have
        # print(f"{monkeys_n=}")
        # print(f"{monkeys_op=}")
        # print(f"{q=}")

    return monkeys_n["root"]


def run_monkeys(humn, monkeys_op, monkeys_n):

    monkeys_n["humn"] = humn
    q = list(monkeys_n.keys())
    while q:
        n_key = q.pop()
        # print(f"Looking where to replace {n_key}")
        # check if we found root
        if n_key == "root":
            # print(f"Found root, likely incorrect. Value {monkeys_n[n_key]}")
            break
        to_remove = []
        for o in monkeys_op:
            if n_key in monkeys_op[o]:
                # found a monkey that has the number key in its formula
                # replace the monkey name with the number
                monkeys_op[o] = tuple(
                    x if x != n_key else monkeys_n[n_key] for x in monkeys_op[o]
                )
                # print(f"Replaced {n_key} in {o}: {monkeys_op[o]}")
                # now check if we found a formula that has two ints in it
                # we can then calculate the result
                if sum(isinstance(x, int) for x in monkeys_op[o]) == 2:
                    # print(f"Found a completed formula! {o}: {monkeys_op[o]}")
                    # add to numbers monkey list

                    # part 2: check if we found root and numbers match
                    if o == "root":
                        return monkeys_op[o]
                    monkeys_n[o] = calc(*monkeys_op[o])
                    q.append(o)
                    # add to removal list
                    to_remove.append(o)

        # remove any processed numbers from the remaining formula monkeys
        for removal in to_remove:
            del monkeys_op[removal]
        # print what we currently have
        # print(f"{monkeys_n=}")
        # print(f"{monkeys_op=}")
        # print(f"{q=}")


def part2_binary_search(monkeys_op, monkeys_n):
    """Solve part 2. Return the required output value."""
    # Part 2:
    # replace 'humn' with an increasing number
    # we use the fact that the formula is linear, so we can use
    # binary search to find the right humn start value.
    monkeys_op_orig = monkeys_op.copy()
    monkeys_n_orig = monkeys_n.copy()
    humn_lo = 0
    humn_high = 40000000000000
    while True:
        humn = humn_lo + ((humn_high - humn_lo) // 2)
        print(f"Trying {humn=}")
        monkeys_op = monkeys_op_orig.copy()
        monkeys_n = monkeys_n_orig.copy()
        result = run_monkeys(humn, monkeys_op, monkeys_n)
        if result[0] == result[2]:
            print(f"Found correct value for humn: {humn=}, {result=}")
            break
        elif result[0] < result[2]:
            # decrease humn - this only works for the actual riddle, not
            # for the test as the test formula is linear (grows for larger
            # values of humn), while the actual riddle formular is inversely
            # linear, i.e. result decreases for higher values of humn
            humn_high = humn_high - ((humn_high - humn_lo) // 2)
            print(f"Too high, trying {humn_lo=} - {humn_high=}")
        elif result[0] > result[2]:
            # increase humn
            humn_lo = humn_lo + ((humn_high - humn_lo) // 2)
            print(f"Too low, trying {humn_lo=} - {humn_high=}")
    # if we get here, a value has been found, but it is not necessarily the
    # lowest possible value as some humn values produce the same result
    # check from current humn_lo to humn if they give the same results
    print(f"Checking further results between {humn_lo} and {humn}")
    for i in range(humn_lo, humn + 1):
        monkeys_op = monkeys_op_orig.copy()
        monkeys_n = monkeys_n_orig.copy()
        result = run_monkeys(humn, monkeys_op, monkeys_n)
        if result[0] == result[2]:
            print(f"Found lowest value for humn with correct result: {i=}, {result=}")
            break
    return i


def solve_for(start, finish, result):
    """Arithmetically solve from start formula to finish formula / value. Value
    is the value the formula in start equates to."""
    if start == finish:
        # atomic case, we have found the search value
        return result
    else:
        left, op, right = global_monkey_formulas[start]
        # extract symbol (to substitute), operator and value from left and right
        reverse = False
        if left in global_monkey_formulas or left == finish:
            # substitution symbol is left of the operator, e.g. result = 'xxxx' + 5
            # we can just revert the operator, even for - and /
            # for result = 'xxxx' - 5, 'xxxx' = result + 5
            # for result = 'xxxx' / 5, 'xxxx' = result * 5
            symbol = left
            value = right
        else:
            assert (right in global_monkey_formulas) or (right == finish)
            # substitution symbol is right of the operator, e.g. result = 5 - 'xxxx'
            # to solve for 'xxxx', for - and / we have to also reverse result and 5
            # for result = 5 - 'xxxx', 'xxxx' = -result + 5 = -1 * result + 5
            # for result = 5 / 'xxxx', 'xxxx' = 5 / result = 5 * 1/result
            symbol = right
            value = left
            reverse = True
        match op:
            case "+":
                result = result - value
            case "*":
                # division is always clean
                assert result % value == 0
                result = result // value
            case "/":
                if reverse:
                    assert value % result == 0
                    result = value // result
                else:
                    result = result * value
            case "-":
                if reverse:
                    result = value - result
                else:
                    result = result + value

        # recursively solve, now starting with symbol
        return solve_for(symbol, finish, result)


@aoc_timer
def part2(monkeys_op, monkeys_n):
    """Solve part 2. Return the required output value."""
    # Part 2:
    # remove the humn value as we are going to solve for it
    del monkeys_n["humn"]

    # do all replacements except for humn. This should then give
    # us a half solved 'root' entry, which we can then solve
    # recursively
    q = list(monkeys_n.keys())
    while q:
        n_key = q.pop()
        # check if we found root
        if n_key == "root":
            break
        to_remove = []
        for o in monkeys_op:
            if n_key in monkeys_op[o]:
                # found a monkey that has the number key in its formula
                # replace the monkey name with the number
                monkeys_op[o] = tuple(
                    x if x != n_key else monkeys_n[n_key] for x in monkeys_op[o]
                )
                # now check if we found a formula that has two ints in it
                # we can then calculate the result
                if sum(isinstance(x, int) for x in monkeys_op[o]) == 2:
                    # add to numbers monkey list
                    monkeys_n[o] = calc(*monkeys_op[o])
                    q.append(o)
                    # add to removal list
                    to_remove.append(o)

        # remove any processed numbers from the remaining formula monkeys
        for removal in to_remove:
            del monkeys_op[removal]

    # solve from root for value of humn
    # extract the substitution symbol and value for root, as
    # root = 'xxxx' == n or root = n == 'xxxx'
    left, _, right = monkeys_op["root"]
    if left in monkeys_op:
        symbol = left
        result = right
    else:
        symbol = right
        result = left
    # create a global copy of the monkeys_op dictionary so it can be referenced
    # in the solve_for function
    global global_monkey_formulas
    global_monkey_formulas = monkeys_op.copy()
    result = solve_for(symbol, "humn", result)

    return result


if __name__ == "__main__":
    # read the puzzle input
    monkeys_op, monkeys_n = load_input("input/21.txt")

    # Solve part 1 and print the answer
    p1 = part1(monkeys_op, monkeys_n)

    print(f"Part 1: {p1}")

    monkeys_op, monkeys_n = load_input("input/21.txt")
    # Solve part 2 and print the answer
    p2 = part2(monkeys_op, monkeys_n)
    print(f"Part 2: {p2}")

# Part 1: Start: 14:09 End: 15:08
# Part 2: Start: 15:10 End: 17:17

# Elapsed time to run part1: 0.15962 seconds.
# Part 1: 353837700405464
# Elapsed time to run part2: 0.16406 seconds.
# Part 2: 3678125408017
