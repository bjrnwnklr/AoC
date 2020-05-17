from collections import defaultdict

class Virus(object):
    def __init__(self, grid):
        self.grid = grid
        self.dir = 0
        self.pos = (0, 0)
        self.burst_count = 0
        self.infect_count = 0

    # class variable that holds the moves by coordinate
    moves = [
        (-1, 0),    # up
        (0, 1),     # right
        (1, 0),     # down
        (0, -1)     # left
    ]

    # infection status is the following
    # 0 = clean
    # 1 = weakened
    # 2 = infected
    # 3 = flagged

    # execute one burst
    def burst(self):
        curr_state = self.grid[self.pos]
        # check if clean
        if curr_state == 0:
            # turn left
            self.dir = (self.dir - 1) % 4
        # check if weakened
        elif curr_state == 1:
            # if weakened, we don't turn but count an infection
            self.infect_count += 1
        # check if infected
        elif curr_state == 2:
            # turn right
            self.dir = (self.dir + 1) % 4
        # node must be infected
        else:
            # reverse direction
            self.dir = (self.dir + 2) % 4

        # change the infected status of current position
        self.grid[self.pos] = (curr_state + 1) % 4

        # move to next grid
        self.pos = (self.pos[0] + Virus.moves[self.dir][0], self.pos[1] + Virus.moves[self.dir][1])

        # increase burst count as we finished one move
        self.burst_count += 1
        

if __name__ == "__main__":
    
    f_name = 'input.txt'

    # read in the grid
    with open(f_name, 'r') as f:
        # infection status is the following
        # 0 = clean
        # 1 = weakened
        # 2 = infected
        # 3 = flagged
        raw_grid = [
            [2 if c == '#' else 0 for c in line.strip('\n').strip()] 
            for line in f.readlines()
        ]

    # find starting position - middle of the grid
    middle = (len(raw_grid) // 2) + 1
    start = (middle, middle)
    

    grid = defaultdict(lambda: False)
    # define the grid (middle is (0, 0), so upper left corner is (-middle+1, -middle+1))
    for r in range(-middle + 1, middle):
        for c in range(-middle + 1, middle):
            grid[(r, c)] = raw_grid[r + (middle - 1)][c + (middle - 1)]

    # instantiate the virus
    virus = Virus(grid)

    cycles = 10_000_000

    for _ in range(cycles):
        virus.burst()

    print(f'Finished {cycles} bursts. Infections recorded: {virus.infect_count}')

# Part 1: 5570
# Part 2: 2512022