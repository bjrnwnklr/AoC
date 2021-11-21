import re
import timeit
from collections import defaultdict


def is_valid(ticket, rules):
    """
    Check if a ticket is valid by checking if all numbers on the ticket match at least one rule
    - outer all: all numbers must match at least one rule
    - middle any: number must match at least one of the rules e.g. "seat" or "class"
    - inner any: number must match at least one of the ranges of the rule e.g. 1-3
    :param ticket: list of ticket numbers to check
    :param rules: dictionary of rules (a rule is a list of two tuples, each tuple is a low and a high range number)
    :return: True if the ticket is valid, i.e. all numbers match at least one rule
    """
    return all(
        any(
            any(
                low <= n <= hi for low, hi in v
            )
            for v in rules.values()
        )
        for n in ticket
    )


def matches_rule(column, rule):
    """
    Check if a list of numbers all match a particular rule.
    :param column: list of numbers to check, this can be a column or a row of numbers
    :param rule: a list with two tuples, each containing a low and high range number
    :return: True if the list of numbers all match the rule.
    """
    for n in column:

        if all(not(low <= n <= hi) for low, hi in rule):
            return False

    return True


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    # f_name = 'ex2.txt'
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

    # create list of all valid tickets by checking which ones have all valid numbers on them
    valid_tickets = [t for t in nearby_tickets if is_valid(t, rules)]

    # for part 2, we now need to compare across columns
    # if any of the values in that column don't work for that particular field, it can't be that field
    # generate a dictionary of the fields, with a list of each column that fits all values

    matching_rules = defaultdict(list)
    for col in range(len(valid_tickets[0])):
        # get all the numbers in that column
        col_nums = [x[col] for x in valid_tickets]

        for rule in rules:
            if matches_rule(col_nums, rules[rule]):
                matching_rules[rule].append(col)

    # starting at the rule that only has one match, eliminate and go through each successive rule
    matched_rules = dict()
    single_rules = [r for r in matching_rules if len(matching_rules[r]) == 1]

    while single_rules:
        # get the next rule entry that only has one matching column, then get the corresponding column
        r = single_rules.pop()
        c = matching_rules[r][0]
        # add the rule / column combination to our dictionary of already found matches
        matched_rules[r] = c
        # remove the rule from the pool of rules to be checked
        matching_rules.pop(r)
        # go through the remaining rules and remove the column from each group of matches
        # (only if that column is contained in any matches - could be that we also have rules that don't contain
        # this particular column
        for rule_to_change in matching_rules:
            if c in matching_rules[rule_to_change]:
                matching_rules[rule_to_change].remove(c)

        # regenerate the list of rules to check - we should have a few more that only have one column
        single_rules = [r for r in matching_rules if len(matching_rules[r]) == 1]

    print(matched_rules)

    # now find all rules that start with "departure"
    departure_fields = [v for k, v in matched_rules.items() if k.startswith('departure')]
    print(departure_fields)

    # multiply the six values at these indices from our own ticket
    part2 = 1
    for i in departure_fields:
        part2 *= own_ticket[i]

    print(f'Part 2: {part2}')

# Part 2: 1515506256421
