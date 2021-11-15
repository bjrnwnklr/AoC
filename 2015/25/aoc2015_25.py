def calc_code(prev_code):
    return (prev_code * 252533) % 33554393

if __name__ == '__main__':

    # solution_row = 6
    # solution_col = 6
    solution_row = 2978
    solution_col = 3083

    # how many numbers do we need to generate?
    # at a maximum, (3083 + 2978) ** 2 // 2
    total_nums = (solution_col + solution_row) ** 2 // 2

    codes = [20151125]
    i = 1
    while i < total_nums:
        codes.append(calc_code(codes[-1]))
        i += 1

    # to find the number in the solution row / column, find the number in the (sol_col + sol_row) - 1 diagonal, then
    # take the sol_col number
    # To find the numbers in the nth diagonal, skip sum(1:n-1) number
    sol_diagonal = solution_row + solution_col - 1
    to_skip = sum(range(1, sol_diagonal))
    solution = codes[to_skip + solution_col - 1]
    print(sol_diagonal, to_skip, solution)

    # Part 1: 2650453
