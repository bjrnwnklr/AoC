from collections import deque

f_name = 'input.txt'

# just for the examples, read multiple groups - one per line. Change for input.txt
with open(f_name, 'r') as f:
    lines = [x.strip('\n') for x in f.readlines()]

for line in lines:

    stream = list(line)

    # stack to store current group level
    stack = deque([])
    curr_level = 0
    group_counter = 0
    score = 0
    garbage = False
    garbage_chars = 0

    while stream:
        # get leftmost character
        c = stream.pop(0)
        # do we have a group opening?
        if c == '{':
            # push current level onto stack
            stack.appendleft(curr_level)
            # increase level by one
            curr_level += 1
        # group closing?
        elif c == '}':
            # increase score by current level
            score += curr_level
            # increase group counter
            group_counter += 1
            # retrieve current_level
            curr_level = stack.popleft()
        # comma - don't increase level
        elif c == ',':
            pass
        # start of garbage
        elif c == '<':
            # process all garbage in here
            garbage = True
            cancel = False
            while garbage:
                g = stream.pop(0)
                # flip cancel statement if '!' found
                if g == '!':
                    cancel = True if not cancel else False
                # close garbage if cancel is False
                elif g == '>' and not cancel:
                    garbage = False
                # pass on all other characters
                else:
                    if not cancel:
                        garbage_chars += 1
                    cancel = False

    # we're done
    print(f'Groups: {group_counter}, score: {score}, non-canceled garbage chars: {garbage_chars}.')

    # Part 1: Groups: 1770, score: 16827.
    # Part 2: non-canceled garbage chars: 7298