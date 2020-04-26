


f_name = 'input.txt'

layers = dict()

with open(f_name, 'r') as f:
    for line in f:
        l, r = map(int, line.strip('\n').split(': '))
        layers[l] = r


def f_scan_pos(x, r):
    s = x % ((r * 2) - 2)
    return s - max(0, s - (r-1)) * 2


# get the max number of layers so we can iterate until the last layer
max_layers = max(layers.keys())
# some variables for tracking our journey
severity = 0
delay = 0

for curr_step in range(max_layers + 1):
    # first move packet to next layer 
    # check if current layer is in layers and if there is a scanner at top of layer
    if (curr_step in layers) and (f_scan_pos(curr_step + delay, layers[curr_step]) == 0):
        severity += curr_step * layers[curr_step]
  
print(f'Reached end, severity score = {severity}')

# Part 1: 1316

while True: 
    # some variables for tracking our journey
    severity = 0
    caught = False

    # now send the package on it's way
    for curr_step in range(max_layers + 1):
        # first move packet to next layer 
        # check if current layer is in layers and if there is a scanner at top of layer
        if (curr_step in layers) and (f_scan_pos(curr_step + delay, layers[curr_step]) == 0):
            severity += curr_step * layers[curr_step]
            # we got caught, move on to next round
            caught = True

    # print(f'Delay {delay}: reached end, severity score = {severity}. Caught: {caught}')

    if not caught:
        print(f'Success with delay {delay}.')
        break

    # increase delay
    delay += 1

# Part 2: 3840052 (takes about 1 minute to calculate!)