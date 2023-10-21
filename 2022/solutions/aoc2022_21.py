# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer


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


# @aoc_timer
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


# @aoc_timer
def part2(monkeys_op, monkeys_n):
    """Solve part 2. Return the required output value."""
    # print(monkeys_op, monkeys_n)
    # process numbers first and replace any occurrence in formulas
    # check if a formula is all numbers, then calculate and add to numbers queue to process
    # Part 2:
    # replace 'humn' with an increasing number
    monkeys_op_orig = monkeys_op.copy()
    monkeys_n_orig = monkeys_n.copy()
    for humn in range(300000):
        monkeys_op = monkeys_op_orig.copy()
        monkeys_n = monkeys_n_orig.copy()
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
                            if monkeys_op[o][0] == monkeys_op[o][2]:
                                # both sides match, stop here
                                print(f"Found correct value: {humn}. {monkeys_op[o]}")
                                return humn
                            else:
                                print(
                                    f"Found incorrect match for root for humn = {humn}. {monkeys_op[o]}"
                                )
                                # else, we do nothing, root will get calculated
                                # after the old formula and pop up
                                # eventually and will go to the
                                # next iteration of humn
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

        # check if root values match

    return -100


if __name__ == "__main__":
    # read the puzzle input
    monkeys_op, monkeys_n = load_input("input/21.txt")

    # Solve part 1 and print the answer
    p1 = part1(monkeys_op, monkeys_n)

    print(f"Part 1: {p1}")

    # Solve part 2 and print the answer
    p2 = part2(monkeys_op, monkeys_n)
    print(f"Part 2: {p2}")

# Part 1: Start: 14:09 End: 15:08
# Part 2: Start: 15:10 End:
