# AOC 2019, day 14
import logging
from collections import defaultdict
import math
import time

def graph_layers(element):
    if element != 'FUEL':
        for x in successors[element]:
            layers[x] = max(layers[x], layers[element] + 1)
            graph_layers(x)



#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    n = 1000
    timings = []
    for _ in range(n):


        # take start time
        start_time = time.time()

        f_name = 'input.txt'

        # process input and generate recipes (format: dict[output element] = [quantity of output, [(input element, quantity)]])
        # successors is a dict of each input element's successors, used to generate a layered graph to select which element to 
        # substitute next 
        recipes = dict()
        successors = defaultdict(list)

        with open(f_name) as f:
            for line in f.readlines():
                inp, outp = line.strip('\n').split(' => ')
                
                # prepare output recipe
                out_q, out_c = outp.split(' ')
                out_q = int(out_q)
                
                # prepare input recipe
                inputs = [(x[1], int(x[0])) for x in (i.split(' ') for i in inp.split(', '))]

                # generate recipe dictionary
                recipes[out_c] = [out_q, inputs[:]]

                # add to graph of successors
                for c, _ in inputs:
                    successors[c].append(out_c)

        logging.debug('Recipes: {}'.format(recipes))
        logging.debug('Successors: {}'.format(successors))


        # generate layers for graph
        # start at ORE and add one layer at a time
        # if value is already there, check if new layer is bigger than previous layer, if yes assign new layer
        layers = defaultdict(int)
        graph_layers('ORE')    
        logging.debug('Layers: {}'.format(layers))

        # needed stores the amount of each element in current recipe
        needed = defaultdict(int)

        # Now process the substitutions
        # starting with FUEL, generate the first recipe
        element = 'FUEL'

        # create a heapq to store the next recipe elements, prioritized by layer (closer to FUEL)
        # since heapq prioritizes by minimum value, use the negative layer value
        rec = [element]
        needed[element] = 1
        logging.debug('rec: {}'.format(rec))

        # run until all elements have been substituted with ORE
        while(set(x for x in rec) - {'ORE'}):

            # get next element from heapq
            r = max(rec, key=lambda x: layers[x])
            rec.remove(r)
            
            # determine multiplicator for recipe quantity
            multiplier = math.ceil(needed[r] / recipes[r][0])

            for el, quantity in recipes[r][1]:
                # append recipe
                needed[el] += quantity * multiplier
                rec.append(el)
                
            needed[r] = 0
            
        # Part 1 done:
        # logging.info('Part 1: {} ORE needed'.format(needed['ORE']))

        elapsed = (time.time() - start_time)
        timings.append(elapsed)

    # calculate average time duration
    avg_duration = sum(timings) / n
    logging.info('Average duration after {} runs: {}'.format(n, avg_duration))


# part 1: 522031