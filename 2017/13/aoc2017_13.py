


f_name = 'input.txt'

layers = dict()

with open(f_name, 'r') as f:
    for line in f:
        l, r = map(int, line.strip('\n').split(': '))
        layers[l] = r

# this calculates the exact position of the scanner depending on the current step (x) and the depth (r)
# we don't need this as we only really want to see if the scanner is at pos 0
def f_scan_pos(x, r):
    s = x % ((r * 2) - 2)
    return s - max(0, s - (r-1)) * 2

# optimized function, calculates if scanner is at position 0
def f_scan_pos_opt(x, r):
    return (x % ((r-1)*2)) == 0


# some variables for tracking our journey
severity = 0
delay = 0

for curr_step in layers.keys():
    # check if current layer is in layers and if there is a scanner at top of layer
    # if (curr_step in layers) and (f_scan_pos(curr_step + delay, layers[curr_step]) == 0):
    if f_scan_pos_opt(curr_step + delay, layers[curr_step]):
        severity += curr_step * layers[curr_step]
  
print(f'Reached end, severity score = {severity}')

# Part 1: 1316

while True: 
    # some variables for tracking our journey
    severity = 0
    caught = False

    # now send the package on it's way
    for curr_step in layers.keys():
        # check if current layer is in layers and if there is a scanner at top of layer
        # if (curr_step in layers) and (f_scan_pos(curr_step + delay, layers[curr_step]) == 0):
        if f_scan_pos_opt(curr_step + delay, layers[curr_step]):
            severity += curr_step * layers[curr_step]
            # we got caught, move on to next round
            caught = True
            break

    if not caught:
        print(f'Success with delay {delay}.')
        break

    # increase delay
    delay += 1

# Part 2: 3840052 (takes about 1 minute to calculate, with optimizations ca 4 seconds.)