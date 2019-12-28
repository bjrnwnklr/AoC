# AOC 2019, day 14
import logging
from collections import defaultdict
import math

#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    f_name = 'input.txt'

    # process input and generate recipes (format: dict[output element] = [left_quantity of output, [(input element, left_quantity)]])
    # `incoming_to` is a dict of each input element's incoming edges, 
    # used to generate a topological sort order 
    recipes = dict()
    incoming_to = defaultdict(list)

    with open(f_name) as f:
        for line in f.readlines():
            left, right = line.strip('\n').split(' => ')
            
            # prepare output recipe
            right_quantity, right_element = right.split(' ')
            right_quantity = int(right_quantity)
            
            # prepare input recipe
            left_ingredients = [(x[1], int(x[0])) for x in (i.split(' ') for i in left.split(', '))]

            # generate recipe dictionary
            recipes[right_element] = [right_quantity, left_ingredients[:]]

            # add to graph of incoming edges
            for left_element, _ in left_ingredients:
                incoming_to[left_element].append(right_element)

    logging.debug('Recipes: {}'.format(recipes))
    logging.debug('incoming_to: {}'.format(incoming_to))

    # needed stores the amount of each element in current recipe
    needed = defaultdict(int)

    # Now process the substitutions
    # starting with FUEL, generate the first recipe
    element = 'FUEL'

    # create a queue to store the next recipe elements, and a dictionary with the quantities needed
    # Set up the starting value as FUEL with quantity 1 - to find out how much ORE is needed to generate 1 FUEL
    recipe_queue = [element]
    needed[element] = 1
    logging.debug('recipe_queue: {}'.format(recipe_queue))

    # Run a topological sort by removing incoming edges from elements that have been substituted
    while(recipe_queue):

        # get next element from heapq
        right_element = recipe_queue.pop()
        
        # determine multiplicator for recipe quantity
        multiplier = math.ceil(needed[right_element] / recipes[right_element][0])

        for left_element, left_quantity in recipes[right_element][1]:
            # append recipe
            needed[left_element] += left_quantity * multiplier
            # remove edge from predecessors
            incoming_to[left_element].remove(right_element)
            # check if no more predecessors, then add to recipe queue
            if not left_element == 'ORE' and not incoming_to[left_element]:
                recipe_queue.append(left_element)
            
        # since we processed the substitution, we don't need any further amount of the substituted element
        needed[right_element] = 0
        
    # Part 1 done:
    logging.info('Part 1: {} ORE needed'.format(needed['ORE']))

# part 1: 522031