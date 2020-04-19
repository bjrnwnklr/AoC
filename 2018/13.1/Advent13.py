my_file = open(r'D:\Python\Advent\13.1\input.txt', 'r').readlines()

class cart:
    t = 0 # number of turns for intersections
    def __init__(self, r, c, d):
        self.r = r # r coordinate (rows)
        self.c = c # c coordinate (columns)
        self.d = d # direction: 0 (up), 1 (right), 2 (down), 3 (left)
        
        
        
    def inter_turn(self):
        self.d = (self.d + turning[self.t]) % 4
        self.t = (self.t + 1) % 3

    def get_pos(self):
        return (self.r, self.c)

    def set_pos(self, r, c):
        self.r = r
        self.c = c

    def set_dir(self, d):
        self.d = d

    def __str__(self):
        return '(%s, %s, %s)' % (self.r, self.c, self.d)

    def move(self):
        x, y = moves[self.d]
        self.r += x
        self.c += y
        # now rotate if required
        underlying = grid[self.r][self.c]
        if underlying == '+':
            self.inter_turn()
        elif underlying == '/':
            if self.d == 0 or self.d == 2: # going up or down
                self.d = (self.d + 1) % 4
            else:                          # has to be going left or right then...
                self.d = (self.d - 1) % 4
        elif underlying == '\\':
            if self.d == 0 or self.d == 2: # going up or down
                self.d = (self.d - 1) % 4
            else:                          # has to be going left or right then...
                self.d = (self.d + 1) % 4
        else:
            pass

        

# definitions
turning = {0: -1, 1: 0, 2: 1} # define dictionary that gives intersection direction
directions = {'^': 0, '>': 1, 'v': 2, '<': 3} # define dictionary of initial directions
moves = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)} # move coordinates based on current direction
replacements = {'^': '|', '>': '-', 'v': '|', '<': '-'} # to replace initial car placements
carts = [] # list of carts
cart_position = set() # set of cart coordinates in tuples (r, c)

# read in grid
grid = [[] for j in range(len(my_file))]
for i in range(len(my_file)):
    grid[i] = [x for x in my_file[i].rstrip('\n')]
    


# find the carts
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] in directions:
            new_cart = cart(i, j, directions[grid[i][j]])
            carts.append(new_cart)
            cart_position.add((i, j))
            # update grid with respective line symbol
            grid[i][j] = replacements[grid[i][j]]


# get sorted list of carts, starting with the one in the top left
carts = sorted(carts, key= lambda cr: (cr.r, cr.c))
print('found %d carts.' % (len(carts)))
print(*carts)
print(*cart_position)

##### part 1 - uncomment

# go through carts and run 1 tick
def part1(carts, cart_position):
    crashed = False
    i = 1
    while not crashed:
        for cr in sorted(carts, key= lambda cr: (cr.r, cr.c)):

            cart_position.remove(cr.get_pos()) # remove the cart from the positions to check for collisions
            cr.move()
            # detect collision
            if cr.get_pos() in cart_position:
                print('COLLISION at (%s, %s) in round %d' % (cr.c, cr.r, i))
                crashed = True
            cart_position.add(cr.get_pos())
        i += 1
        


##### part 2
def part2(carts, cart_position):
    collided = set()
    i = 1
    while len(carts) > 1:
        for cr in sorted(carts, key= lambda cr: (cr.r, cr.c)):
            if not cr in collided: 
                cart_position.remove(cr.get_pos()) # remove the cart from the positions to check for collisions
                cr.move()
                # detect collision
                if cr.get_pos() in cart_position: # we have found a collision
                    print('COLLISION at (%s, %s) in round %d' % (cr.r, cr.c, i))
                    carts.remove(cr) # remove the current cart from the list of carts
                    cart_position.remove(cr.get_pos())
                    collided.add(cr)
                    print('# of carts left: %d' % (len(carts)))
                    print(*carts)
                    for o_cr in carts:
                        if o_cr.get_pos() == cr.get_pos():    # remove collided cart from list of carts too
                            carts.remove(o_cr)
                            collided.add(o_cr)
                            print('\tRemoved another cart: %s' % (o_cr))
                else:
                    cart_position.add(cr.get_pos())
        i += 1
    # we have only cart left, report back
    return (carts[0].c, carts[0].r)

#part1(carts, cart_position)
print('Last cart left at (%s, %s).' % (part2(carts, cart_position)))

