

f_name = 'input.txt'

layers = dict()

with open(f_name, 'r') as f:
    for line in f:
        l, r = map(int, line.strip('\n').split(': '))
        layers[l] = r


# create firewall based on each layer and range of scanning area, including empty layers
# each firewall layer has a number of where the scanner currently is, starting at 0
# empty layers are all at 0 and will be skipped when advancing the scanner
# get the max number of layers
max_layers = max(layers.keys())
firewall = [0] * (max_layers + 1)
# start with direction -1 (going up). This will be reversed on the first run
directions = [-1] * (max_layers + 1)
# some variables for tracking our journey
severity = 0

for curr_step in range(max_layers + 1):
    # first move packet to next layer 
    # check if current layer is in layers and if there is a scanner at top of layer
    if (curr_step in layers) and (firewall[curr_step] == 0):
        severity += curr_step * layers[curr_step]
  
    # now move each scanner to next step
    # change direction when firewall scanner is at either 0 or (range - 1) (top or bottom)
    for i in layers.keys():
        if firewall[i] == 0 or firewall[i] == (layers[i] - 1):
            directions[i] *= -1
        
        # move scanner to next level
        firewall[i] += directions[i]

print(f'Reached end, severity score = {severity}')

# Part 1: 1316

delay = 0


while True:
    max_layers = max(layers.keys())
    firewall = [0] * (max_layers + 1)
    # start with direction -1 (going up). This will be reversed on the first run
    directions = [-1] * (max_layers + 1)
    # some variables for tracking our journey
    severity = 0
    caught = False

    # run firewall scanners while delay
    for d in range(delay):
        for i in layers.keys():
            if firewall[i] == 0 or firewall[i] == (layers[i] - 1):
                directions[i] *= -1
            
            # move scanner to next level
            firewall[i] += directions[i]

    # now send the package on it's way
    for curr_step in range(max_layers + 1):
        # first move packet to next layer 
        # check if current layer is in layers and if there is a scanner at top of layer
        if (curr_step in layers) and (firewall[curr_step] == 0):
            severity += curr_step * layers[curr_step]
            # we got caught, move on to next round
            caught = True
    
        # now move each scanner to next step
        # change direction when firewall scanner is at either 0 or (range - 1) (top or bottom)
        for i in layers.keys():
            if firewall[i] == 0 or firewall[i] == (layers[i] - 1):
                directions[i] *= -1
            
            # move scanner to next level
            firewall[i] += directions[i]

    # print(f'Delay {delay}: reached end, severity score = {severity}. Caught: {caught}')

    if not caught:
        print(f'Success with delay {delay}.')
        break

    # increase delay
    delay += 1

