from collections import deque, defaultdict





def generate_grid(y, x, fav_number):
    # generate a grid based on the fav number (puzzle input)
    return [[is_wall(r, c, fav_number) for c in range(x+1)] for r in range(y+1)]
    

def is_wall(r, c, fav_number):
    checksum = c ** 2 + 3 * c + 2 * c * r + r + r ** 2 + fav_number
    bin_num = f'{checksum:b}'
    ones = sum(1 if x == '1' else 0 for x in bin_num)
    return True if ones % 2 != 0 else False

def draw_grid(grid):
    for r in range(len(grid)):
        print(''.join(['#' if grid[r][c] else '.' for c in range(len(grid[0]))]))


puzzle_input = 1350
start = (1, 1)
target = (39, 31)
grid = generate_grid(51, 51, puzzle_input)

# find the shortest route using BFS
path = defaultdict(list)
seen = set()
steps = 0
fifty_steps = 0
q = deque([(start, steps, [])])

while q:
    curr_pos, curr_steps, curr_path = q.pop()

    if curr_pos in seen:
        continue

    seen.add(curr_pos)
    # for part 2, count how many positions can be reached in at most 50 steps
    if curr_steps <= 50:
        fifty_steps += 1

    for next_pos in [(curr_pos[0] + n[0], curr_pos[1] + n[1]) for n in [
        (1, 0),
        (0, -1),
        (-1, 0),
        (0, 1)]
        ]:
        # check if all coordinates > 0 and within grid, if no wall, and if we have not found this in another path already
        if (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0])
            and not grid[next_pos[0]][next_pos[1]]
            and next_pos not in seen
            and next_pos not in path):
            # add to path
            path[next_pos] = curr_path + [next_pos]
            q.appendleft([next_pos, curr_steps + 1, curr_path + [next_pos]])


print('Done')
print(f'Reachable in <= 50 steps: {fifty_steps}.')

# part 1: 92 steps
# part 2: 124 locations reachable in <= 50 steps
