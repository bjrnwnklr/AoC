import re
import timeit


def solve_part1_sets(rules, flat_nearby_tickets):
    # Part 1:
    # - create ranges of the valid values in all fields
    # - check which number is in none of the ranges by using sets
    all_valid_ranges = []

    for v in rules.values():
        rules_ranges = set()
        for low, hi in v:
            rules_ranges |= {*range(low, hi + 1)}
        all_valid_ranges.append(rules_ranges)

    # now check each number from nearby tickets against all the ranges
    invalid_nums = []
    for n in flat_nearby_tickets:
        if all(n not in r for r in all_valid_ranges):
            invalid_nums.append(n)

    return invalid_nums


def solve_part1_comp(rules, flat_nearby_tickets):
    # alternative way without sets
    invalid_nums = []
    for n in flat_nearby_tickets:
        valid = False
        for v in rules.values():
            for low, hi in v:
                if low <= n <= hi:
                    valid = True
                    break
            if valid:
                break

        if not valid:
            invalid_nums.append(n)

    return invalid_nums



if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        raw_rules, raw_own_ticket, raw_nearby_tickets = f.read().split('\n\n')

    # read in the rules
    rules = dict()

    for line in raw_rules.split('\n'):
        field, vals = line.split(': ')
        vals = vals.split(' or ')
        val_ranges = [tuple(map(int, re.findall(r'(\d+)', v))) for v in vals]
        rules[field] = val_ranges

    # read in my ticket
    own_ticket = list(map(int, raw_own_ticket.split('\n')[1].strip('\n').split(',')))

    # read in nearby tickets (the [1:-1] is required to remove the "nearby tickets" line at the beginning
    # and the last empty line at the end of the file, as that empty line belongs to the raw_nearby_tickets field
    nearby_tickets = []
    for line in raw_nearby_tickets.split('\n')[1:-1]:
        nearby_tickets.append(list(map(int, line.strip('\n').split(','))))

    # create flat list of nearby ticket values
    flat_nearby_tickets = [x for tick in nearby_tickets for x in tick]

    t = 1000
    start_time = timeit.default_timer()
    for _ in range(t):
        invalid_nums = solve_part1_sets(rules, flat_nearby_tickets)
    print((timeit.default_timer() - start_time) / t)
    print(f'Part 1: ticket scanning error rate: {sum(invalid_nums)}')

    start_time = timeit.default_timer()
    for _ in range(t):
        invalid_nums = solve_part1_comp(rules, flat_nearby_tickets)
    print((timeit.default_timer() - start_time) / t)
    print(f'Part 1: ticket scanning error rate: {sum(invalid_nums)}')

# Part 1: ticket scanning error rate: 26053
# 0.0026285628 (avg time to solve using sets)
# 0.0160892069 (avg time to solve using comparisons)
# 0.0012469923 (avg time using optimized comparisions (breaking out once a valid number found)
