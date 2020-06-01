from collections import deque


elements = [
    'H', 'L'
]

devices = [
    'M', 'G'
]

def get_moves(current_state):
    # iterate through all possible moves (go up/down a floor and take one or two elements)
    # and then check if it is a possible move

    # what is on the current floor?
    elevator, microchips, generators = current_state
    for el in (microchips, generators):
        for i, d in enumerate(el):
            if d == elevator:



# state is 
# - elevator floor
# - HM
# - LM
# - HG
# - LG
state = (1, 11, 23)
# everything on 4th floor
end = (4, 44, 44)


# run a BFS to find the end state
# q contains:
# - state (where is everything)
# - number of moves
q = deque([state, 0])
seen = set()

while q:
    current_state, current_moves = q.pop()

    if current_state in seen:
        continue

    if current_state == end:
        # we found the end state
        print(f'End state found, number of moves: {current_moves}')
        break

    # add to seen
    seen.add(current_state)

    # select next moves
    for next_move in get_moves(current_state):
        q.appendleft((next_move, current_moves + 1))

print('Done.')