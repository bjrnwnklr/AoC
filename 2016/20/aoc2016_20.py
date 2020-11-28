import re

# read in the numbers into a list of tuples
# sort the list by lowest number (first number in tuple)
# then compare against minimum available number

f_name = 'input.txt'
# f_name = 'ex1.txt'

with open(f_name, 'r') as f:
    ranges = [tuple(map(int, re.findall(r'(\d+)', line))) for line in f.readlines()]

# sort the ranges by smallest value of the first in the tuple
ranges = sorted(ranges, key=lambda x: x[0], reverse=False)

print(ranges[0:10])

# check each tuple against the current minimal value and pick the higher tuple + 1 if current minimum is with
# blacklist range
curr_min = 0
for blacklist_range in ranges:
    if blacklist_range[0] <= curr_min:
        curr_min = blacklist_range[1] + 1

print(curr_min)

# Part 1: 32259706

# Try a different approach for part 2 - consolidate ranges where possible
finished = False


while not finished:
    range_count = len(ranges)
    curr_l, curr_h = ranges.pop(0)
    consolidated_ranges = []
    while ranges:
        next_l, next_h = ranges.pop(0)
        if curr_l <= next_l <= curr_h + 1:
            if curr_h <= next_h:
                curr_h = next_h
        # we found a new range outside our current range
        else:
            consolidated_ranges.append([curr_l, curr_h])
            curr_l, curr_h = next_l, next_h

    # we have gone through each element of ranges and all ranges are now in the consolidated_ranges object
    # but we need to also add the last current values
    consolidated_ranges.append([curr_l, curr_h])
    # now sort the consolidated ranges into a new ranges object
    ranges = sorted(consolidated_ranges, key=lambda x: x[0])
    # if the count of ranges stays constant we are done
    if range_count == len(ranges):
        finished = True

print(ranges)

# now count ranges between the ranges
low_count = 0
ip_count = 0
for curr_l, curr_h in ranges:
    ip_count += len(range(low_count, curr_l))
    low_count = curr_h + 1

print(ip_count)

# Part 2: 113
