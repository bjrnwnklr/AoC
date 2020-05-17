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

    # execute one burst
    def burst(self):
        # check if infected, if yes, turn right, otherwise turn left
        if self.grid[self.pos]:
            self.dir = (self.dir + 1) % 4
        else:
            self.dir = (self.dir - 1) % 4
            # increase the count of infections by one
            self.infect_count += 1

        # flip the infected status of current position
        self.grid[self.pos] = not self.grid[self.pos]

        # move to next grid
        self.pos = (self.pos[0] + Virus.moves[self.dir][0], self.pos[1] + Virus.moves[self.dir][1])

        # increase burst count as we finished one move
        self.burst_count += 1
        

if __name__ == "__main__":
    
    f_name = 'input.txt'

    # read in the grid
    with open(f_name, 'r') as f:
        raw_grid = [
            [True if c == '#' else False for c in line.strip('\n').strip()] 
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

    cycles = 10_000

    for _ in range(cycles):
        virus.burst()

    print(f'Finished {cycles} bursts. Infections recorded: {virus.infect_count}')

# Part 1: 5570
