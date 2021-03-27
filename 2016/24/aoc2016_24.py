from collections import deque


def set_bit(bitmask, bit_to_set):
    return bitmask | 1 << bit_to_set


# f_name = 'ex1.txt'
f_name = 'input.txt'

grid = set()
wires = dict()
with open(f_name, 'r') as f:
    for r, line in enumerate(f.readlines()):
        for c, x in enumerate(list(line.strip())):
            if x != '#':
                grid.add((r, c))
                if x != '.':
                    wires[(r, c)] = int(x)
                if x == '0':
                    start = (r, c)


# Idea: use a BFS with a combination of position and wires visited. Repeat until
# the end state (= all wires visited) has been reached.

# generate a bitmask of the final state i.e. all wires have been visited
# If all wires were numbered consecutively, we could take (2 ** the highest number+1) - 1
# e.g. 2**(4+1) - 1 = 31 if 4 was the highest number
def bfs(grid, wires, start, part):
    endstate = 0
    for b in wires.values():
        endstate = set_bit(endstate, b)
    # startmask is 1, i.e. the 0 bit is already set as we are already on the 0 position and
    # don't need to visit it again.
    startmask = 1
    q = deque([((start, startmask), 0)])
    seen = set()

    while q:
        current_pos, current_steps = q.pop()

        if current_pos in seen:
            continue
        seen.add(current_pos)

        if current_pos[1] == endstate:
            # For part 1, it is sufficient to just reach visit each wire (i.e. endstate bitmask is all 1s)
            # For part 2, we need to have visited all wires (i.e. endstate bitmask is all 1s) and we need to be
            # on the start position. This can be a completely different path than the one taken for part 1.
            if (part == 1) or (part == 2 and current_pos[0] == start):
                # we found the endstate, break and finish
                print(f'BFS finished, number of steps: {current_steps}')
                print(f'Current position is: {current_pos[0]}')
                if current_pos[0] in wires:
                    print(f'on top of wire {wires[current_pos[0]]}')
                return current_steps

        for neighbor_pos in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            next_pos = (current_pos[0][0] + neighbor_pos[0], current_pos[0][1] + neighbor_pos[1])
            if next_pos in grid:
                # check if we are on a wire and set the bit for the wire
                if next_pos in wires:
                    next_state = set_bit(current_pos[1], wires[next_pos])
                else:
                    next_state = current_pos[1]
                q.appendleft(((next_pos, next_state), current_steps + 1))


# BFS finished and should have found the shortest path
part1_steps = bfs(grid, wires, start, 1)
print(f'Part 1: {part1_steps}')
# Part 1: 500

part2_steps = bfs(grid, wires, start, 2)
print(f'Part 2: {part2_steps}')
# Part 2: 748
