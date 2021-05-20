from itertools import combinations
from functools import reduce


def get_one_third(req_weight, all_candidates):
    # find all possible combinations for the first group that add up to one_third
    for i in range(1, len(all_candidates)):
        for c in combinations(all_candidates, i):
            if sum(c) == req_weight:
                # print(tuple(c))
                yield c


def quantum_entanglement(packages):
    return reduce(lambda x, y: x * y, packages)


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

    # valid_combinations = []
    # min_number_of_packages = 100 # set an initial high value to compare least number of packages against
    # pass_gen = get_one_third(one_third, weights)
    # while True:
    #     # get the next combination of packages that weigh one third. The generator will yield combinations with
    #     # least number of packages first, ascending to more packages
    #     pass_comp = next(pass_gen)
    #
    #     # which packages are left over - again find the second group that weighs the same
    #     remaining_packages = weights - set(pass_comp)
    #     sec_gen = get_one_third(one_third, remaining_packages)
    #     while True:
    #         second_comp = next(sec_gen)
    #         # get the last group of leftover packages. We now need to only check if we can find one
    #         # combination that weighs the same (one third) and we know it satisfies all criteria. No
    #         # need to search further for this group of packages
    #         last_group = remaining_packages - set(second_comp)
    #         if sum(last_group) == one_third:
    #             valid_combinations.append(pass_comp)
    #             break
    #
    #     # check if the last valid combination had more packages than the current minimum
    #     # if yes, we can stop searching
    #     if len(valid_combinations[-1]) > min_number_of_packages:
    #         # if the last valid result has more packages, remove it and stop as we don't need to go
    #         # through combinations with more packages
    #         valid_combinations.pop()
    #         break
    #     else:
    #         min_number_of_packages = len(valid_combinations[-1])
    #
    # print(min(quantum_entanglement(x) for x in valid_combinations))

    # Part 1: 11266889531

    # Part 2
    one_quarter = total_weight // 4

    valid_combinations = []
    min_number_of_packages = 100 # set an initial high value to compare least number of packages against
    pass_gen = get_one_third(one_quarter, weights)
    while True:
        # get the next combination of packages that weigh one third. The generator will yield combinations with
        # least number of packages first, ascending to more packages
        pass_comp = next(pass_gen)

        # which packages are left over - again find the second group that weighs the same
        remaining_packages = weights - set(pass_comp)
        sec_gen = get_one_third(one_quarter, remaining_packages)
        while True:
            second_comp = next(sec_gen)
            third_remaining_packages = remaining_packages - set(second_comp)
            third_gen = get_one_third(one_quarter, third_remaining_packages)
            while True:
                third_comp = next(third_gen)
                # get the last group of leftover packages. We now need to only check if we can find one
                # combination that weighs the same (one third) and we know it satisfies all criteria. No
                # need to search further for this group of packages
                last_group = third_remaining_packages - set(third_comp)
                if sum(last_group) == one_quarter:
                    valid_combinations.append(pass_comp)
                    break

            # check if the last valid combination had more packages than the current minimum
            # if yes, we can stop searching
            if len(valid_combinations[-1]) > min_number_of_packages:
                # if the last valid result has more packages, remove it and stop as we don't need to go
                # through combinations with more packages
                break
            else:
                min_number_of_packages = len(valid_combinations[-1])

        if len(valid_combinations[-1]) > min_number_of_packages:
            # if the last valid result has more packages, remove it and stop as we don't need to go
            # through combinations with more packages
            valid_combinations.pop()
            break

    print(min(quantum_entanglement(x) for x in valid_combinations))