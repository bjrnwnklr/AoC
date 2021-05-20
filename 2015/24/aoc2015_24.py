from itertools import combinations


def get_one_third(req_weight, all_candidates):
    # find all possible combinations for the first group that add up to one_third
    for i in range(1, len(all_candidates)):
        for c in combinations(all_candidates, i):
            if sum(c) == req_weight:
                # print(tuple(c))
                yield c


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        weights = {
            int(x.strip()) for x in f.readlines()
        }

    # get the sum of the packages, divide by 3 to find out how much they are allowed
    # to weigh
    total_weight = sum(weights)
    one_third = total_weight // 3
    print(total_weight, one_third)

    pass_gen = get_one_third(one_third, weights)
    while True:
        pass_comp = next(pass_gen)
        print(pass_comp)
        remaining_packages = weights - set(pass_comp)
        found = False
        sec_gen = get_one_third(one_third, remaining_packages)
        while not found:
            second_comp = next(sec_gen)
            last_group = remaining_packages - set(second_comp)
            if sum(last_group) == one_third:
                print(f'Found: {pass_comp}, {second_comp}, {last_group}')