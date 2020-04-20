import re
import heapq
from collections import defaultdict
import math

# read in file
f_name = 'input.txt'

# use topological sort
# 1. put all input values into a structure with incoming and outgoing edges
# 2. find the node that has no incoming edges

above = defaultdict(list)
below = defaultdict(list)
weights = dict()

with open(f_name, 'r') as f:
    for line in f:
        # split along -> into two parts if this is present in the line
        if '->' in line:
            left, right = line.strip('\n').split(' -> ')
            balancing = [x.strip() for x in right.split(',')]
        else:
            left = line.strip('\n')
            balancing = []

        pgm, weight = re.match('([a-z]+)\s\((\d+)\)', left).groups()
        weights[pgm] = int(weight)
        # print(pgm, weight, balancing)

        # add into graph: anything where balancing has elements will be processed
        # - anything in balancing will be added to "above" dictionary
        # - any prgm that has balancing will be added to "below"
        for b in balancing:
            below[b].append(b)
        above[pgm] = balancing

# now find the one element that has no "below"
start_nodes = [x for x in above if x not in below]

print(start_nodes)

# part 1: vmpywg

def tower_sum(node):
    # end condition: if nothing above, return weight
    if not above[node]:
        # print(f'Nothing above node {node}, returning weight {weights[node]}.')
        return weights[node]
    else:
        # recurse through nodes above
        above_weights = [tower_sum(n) for n in above[node]]
        # check if all weights above have the same weight
        max_weight = max(above_weights)
        min_weight = min(above_weights)
        if max_weight != min_weight:
            print(f'Above node {node}, not all have same weight! {above_weights}')

            # identify the wrong weight by subtracting the min from each weight.
            # This should be 0 for all but one. The absolute of this value is the delta we
            # need to take off. Identify the weight from the index of the non zero value
            minus_min = [x - min_weight for x in above_weights]
            delta = [x for x in minus_min if x != 0][0]
            index_delta = minus_min.index(delta)
            faulty_node = above[node][index_delta]
            faulty_weight = weights[faulty_node]
            new_weight = faulty_weight - delta
            print(f'Faulty weight related to node {faulty_node} (at index {index_delta}): {faulty_weight} needs to be {delta}: {new_weight}.')

        # print(f'Summed up above node {node}, returning weight {sum(above_weights) + weights[node]}')
        return sum(above_weights) + weights[node]

total_weight = tower_sum(start_nodes[0])

print(total_weight)

# part 2: 1674 (Faulty weight related to node ncrxh (at index 4): 1679 needs to be 5: 1674.)