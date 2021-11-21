import aoctools


def transform_subject_number_memo(subject_number, loop_size, memo):

    divider = 20201227

    if loop_size == 1:
        value = 1
    else:
        value = memo[loop_size - 1]

    value *= subject_number
    value %= divider

    memo[loop_size] = value

    return value

@aoctools.aoc_timer
def solve_memo(inp):
    public_keys = inp
    memo = dict()

    loop_sizes = []
    for pk in public_keys:
        cycles = 1
        subject_number = 7
        while transform_subject_number_memo(subject_number, cycles, memo) != pk:
            cycles += 1
            # if cycles % 100_000 == 0:
            #     print(cycles)
        print(pk, cycles)
        loop_sizes.append(cycles)

    print(loop_sizes)
    # get the final encryption key
    enc_keys = []
    for i, pk in enumerate(public_keys):
        enc_keys.append(pow(pk, loop_sizes[(i + 1) % 2], 20201227))

    print(enc_keys)


@aoctools.aoc_timer
def solve_loop(inp):
    public_keys = inp
    divider = 20201227
    subject_number = 7

    cycles = 0
    value = 1
    loop_sizes = []
    for pk in public_keys:
        while value != pk:
            value *= subject_number
            value %= divider
            cycles += 1
        print(pk, cycles)
        loop_sizes.append(cycles)

    print(loop_sizes)
    enc_keys = []
    for i, pk in enumerate(public_keys):
        enc_keys.append(pow(pk, loop_sizes[(i + 1) % 2], 20201227))

    print(enc_keys)


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'


    with open(f_name, 'r') as f:
        public_keys = list(map(int, f.readlines()))

    solve_memo(public_keys[:])

    solve_loop(public_keys[:])




    # Part 1: 18433997 (takes a few minutes using the pow function; much longer if using manual implementation)
    # The fastest way is (as usual!) to use memoization and just store the result from each calculation, as we
    # go back to the calculation for loop_size + 1 and re-use the already calculated value for loop_size.
