# AOC 2019, day 14
import logging
from collections import defaultdict
import math

def graph_layers(element):
    if element != 'FUEL':
        for x in successors[element]:
            layers[x] = max(layers[x], layers[element] + 1)
            graph_layers(x)



#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    f_name = 'ex3.txt'

    # process input and generate recipes (format: dict[output element] = [quantity of output, [(input element, quantity)]])
    # successors is a dict of each input element's successors, used to generate a layered graph to select which element to 
    # substitute next 
    recipes = dict()
    successors = defaultdict(list)

    with open(f_name) as f:
        for line in f.readlines():
            inp, outp = line.split(' => ')
            
            # prepare output recipe
            out_q, out_c = outp.split(' ')
            out_q = int(out_q)
            out_c = out_c.strip('\n')
            
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

    # Now process the substitutions
    # starting with FUEL, generate the first recipe
    element = 'FUEL'

    _, rec = recipes[element]
    logging.debug('rec: {}'.format(rec))

    # run until all elements have been substituted with ORE
    while(set(x[0] for x in rec) - {'ORE'}):

        
        # check which of the elements can be substituted with multiples of the recipe output
        subs = [x[0] for x in rec if x[0] != 'ORE' and x[1] % recipes[x[0]][0] == 0]
        logging.debug('Subs: {}'.format(subs))

        # check if we need to do a wasteful substitution - only of no clean subs found
        if not subs:
            logging.debug('No more subs!')
            sub_candidates = [x[0] for x in rec if x[0] != 'ORE']
            subs = [max(sub_candidates, key=lambda x: layers[x])]
            logging.debug('Next wasteful substitution: {}'.format(subs))

        next_rec = []  
        for r in rec:
            if not r[0] in subs:
                next_rec.append(r)
            else:
                # determine multiplicator for recipe quantity
                multiplier = math.ceil(r[1] / recipes[r[0]][0])
                # append recipe
                next_rec.extend([(x[0], x[1] * multiplier) for x in recipes[r[0]][1]])

        rec = next_rec
        logging.debug('After subs: {}'.format(rec))

        # Add all same elements together
        rec = [(e, sum(q[1] for q in rec if q[0] == e)) for e in set(x[0] for x in rec)]
        logging.debug('New_rec: {}'.format(rec))

    # Part 1 done:
    logging.info('Part 1: {} ORE needed'.format(rec[0][1]))

# part 1: 522031