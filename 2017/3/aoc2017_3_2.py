from collections import defaultdict

i = 2
sidelength = 3
steps_left = 1
grid = defaultdict(int, {(0, 0): 1})
dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]
current_pos = (0, 1)
current_score = 0
current_dir = 0

n = 368078

while (current_score < n):
    # update score of current position
    current_score = sum(grid[r, c] for r in range(current_pos[0] - 1, current_pos[0] + 2)
        for c in range(current_pos[1] - 1, current_pos[1] + 2))
    grid[current_pos] = current_score

    # move to next position
    # first check if we are on a square of the sidelength (lower right corner)
    if (i == sidelength ** 2):
        # change position to move to the right
        current_pos = (current_pos[0], current_pos[1] + 1)
        # add 2 to sidelength 
        sidelength += 2
        # steps left is sidelength - 2
        steps_left = sidelength - 2
        # current direction is upwards (index 0)
        current_dir = 0
    elif steps_left == 0:
        # turn if steps_left == 0 - meaning we are at a corner.
        current_dir += 1
        # move into next position
        current_pos = (current_pos[0] + dirs[current_dir][0], current_pos[1] + dirs[current_dir][1])
        # steps_left starts again at sidelength - 2
        steps_left = sidelength - 2
    else:
        # there are still steps left on the side, so move 1 in current direction
        current_pos = (current_pos[0] + dirs[current_dir][0], current_pos[1] + dirs[current_dir][1])
        steps_left -= 1
    # move to next step
    i += 1

print(f'Done. {i}: {current_score}')