# Day 15: Beverage Bandits
# part 2:
# After increasing the Elves' attack power until it is just
# barely enough for them to win without any Elves dying,
# what is the outcome of the combat described in your puzzle input?


from collections import defaultdict, deque

################ global constants #######################
n_coords = [(-1, 0), (0, -1), (0, 1), (1, 0)]

################ CLASS definitions ######################
class Unit:
    hp = 200        # hitpoints
    ap = 3          # attack power
    utype = ''      # unit type (Elf or Goblin)
    alive = True    # status - alive or dead
    
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def __str__(self):
        return '%s:(%d, %d):%d' % (self.utype, self.r, self.c, self.hp)

    def get_pos(self):
        return (self.r, self.c)

    # returns coordinates of any squares around that are not walls (but includes other units!)
    def open_sq(self):
        return [(r, c) for r, c in [(self.r + y, self.c + x) for y, x in n_coords] if grid[(r, c)] == 0]

    def isAlive(self):
        return self.alive

    def get_type(self):
        return self.utype

    def get_hp(self):
        return self.hp

    def move(self, r, c):
        if (r, c) in self.open_sq():
            #print('%s moving to (%d, %d)' % (self, r, c))
            self.r = r
            self.c = c

    def attack_next(self, units):
        next_to = [e for e in units if e.utype == enemy_type[self.get_type()] 
                    and e.isAlive() 
                    and self.get_pos() in e.open_sq()]
        return sorted(next_to, key = lambda u: (u.get_hp(), u.get_pos()))

    def take_hit(self, ap):
        self.hp -= ap
        if self.hp <= 0:
            self.alive = False
            

class Goblin(Unit):
    utype = 'G'

class Elf(Unit):
    utype = 'E'

    # overload the constructor to allow custom attack points for elves
    def __init__(self, r, c, elf_ap = 3):
        self.r = r
        self.c = c
        self.ap = elf_ap

    # overload the take_hit method - throw an exception if an elf dies
    def take_hit(self, ap):
        self.hp -= ap
        if self.hp <= 0:
            self.alive = False
            raise ElfDeadException('Elf %s died!' % self)


class ElfDeadException(Exception):
        def __init__(self, message):
            self.message = message

################## Helper functions ##############

# some useful definitions
types = {0: '.', 1: '#'}
enemy_type = {'G': 'E', 'E': 'G'}


def print_grid(grid, units):
    max_r = max(r for r, _ in grid.keys())
    max_c = max(c for _, c in grid.keys())
    elves = [u.get_pos() for u in units if u.utype == 'E' and u.isAlive()]
    goblins = [u.get_pos() for u in units if u.utype == 'G' and u.isAlive()]
    for r in range(max_r + 1):
        line = ''
        for c in range(max_c + 1):
            if (r, c) in elves:
                x = 'E'
            elif (r, c) in goblins:
                x = 'G'
            else:
                x = types[grid[(r, c)]]
            line += x
        print(line)

def BFS(grid, start, all_units):
    q = deque([(start, [])])
    seen = set()
    paths = defaultdict(list)
    while q:
        v1, p = q.pop() # removes element from the right side of the queue
        if v1 not in seen:
            seen.add(v1)
            #new_p = p + [v1] # add the current grid to the path (make sure to use a copy of the path!)

            # find all valid neighbours
            for n in n_coords:
                v_next = (v1[0] + n[0], v1[1] + n[1])
                if (v_next in grid 
                    and v_next not in seen
                    and v_next not in paths ### key change - if this is not in, BFS overwrites existing paths
                                            ### which destroys reading order
                    and grid[v_next] != 1
                    and v_next not in all_units):
                    # push into queue - on the left side
                    # set the path to this new square
                    paths[v_next] = p + [v_next]
                    q.appendleft((v_next, p + [v_next]))

                  
    # once q is empty, return the dictionary with paths
    return paths

############### CODE ################################
def load(elf_ap):
    grid = dict()
    units = []
    my_file = open(r'test_inputs.txt', 'r')
    for r, l in enumerate(my_file):
        for c, x in enumerate(l.rstrip()):
            if x == '#':
                sq = 1
            elif x == '.':
                sq = 0
            elif x == 'G':
                sq = 0
                units.append(Goblin(r, c))
            elif x == 'E':
                sq = 0
                units.append(Elf(r, c, elf_ap))
            grid[(r, c)] = sq


    units.sort(key = lambda u: (u.r, u.c))
    return grid, units


########### sequence of events #############
# 1) check list of remaining targets - if no targets available, end the whole program
# 2) identify open squares next to targets
# 3) identify if next to a target
# 4) if no open squares and not next to a target, end turn
# 5) if next to a target, attack, otherwise move
# 6) consider which open squares are closest (BFS, if equal length use reading order)
# 7) take one step towards the nearest goal (reading order if > 1 are nearest)
# 8) attack after moving if now in range - if not, end turn


elf_ap = 4
while True:
    grid, units = load(elf_ap)

    try:
        combat_end = False
        rounds = 0
        while not combat_end:
            for u in units:
                if u.isAlive():
                    # 1) identify targets that are still alive
                    enemies = [e for e in units if e.utype == enemy_type[u.utype] and e.isAlive()]
                    all_units = [n.get_pos() for n in units if n.isAlive()]
                    if not enemies:
                        combat_end = True
                        break
                    # 2) identify open squares next to targets and if we are next to a target
                    pot_squares = [n for e in enemies for n in e.open_sq() if n not in all_units]
                    next_to = u.attack_next(units)
                    #print('%s sees %d potential squares: %s' % (u, len(pot_squares), pot_squares))
                    #print('%s is next to %d enemies: %s' % (u, len(next_to), next_to))
                    # 4) if no open squares and not next to a target, end turn
                    if not next_to and not pot_squares:
                        #print('%s ends turn' % u)
                        continue
                    elif next_to:
                        # select next target (lowest hp, then reading order) and attack
                        to_attack = next_to[0]
                        #print('%s attacks %s' % (u, to_attack))
                        to_attack.take_hit(u.ap)
                    elif pot_squares:
                        # 6) move... consider nearest target (use BFS)
                        paths = BFS(grid, u.get_pos(), all_units)
                        to_move = [n for n in pot_squares if len(paths[n]) > 0]
                        if to_move:
                            nearest_target = sorted(to_move, key = lambda n: (len(paths[n]), n))[0]
                            #print('%s found %d potential moves, nearest is %s with %d steps' % (u, len(to_move), nearest_target, len(paths[nearest_target])))
                            # now move... select the first entry in the sorted paths dictionary - the shortest
                            # and in reading order
                            u.move(*paths[nearest_target][0])
                            # and attack if now next to an enemy
                            next_to = u.attack_next(units)
                            if next_to:
                                to_attack = next_to[0]
                                #print('%s attacks %s' % (u, to_attack))
                                # attack this unit, then turn ends
                                to_attack.take_hit(u.ap)
                        else: 
                            #print('%s found no potential moves, ending turn' % u)
                            continue # no reachable targets, end turn
            # a round finished without ending the combat. increase rounds, resort the units into reading order
            # and start the next round
            if not combat_end: 
                rounds += 1
                units.sort(key = lambda u: (u.r, u.c))
    
    # catch the exception if an elf has died and restart with increased elf attack power
    except ElfDeadException as elf_dead_exception:
        #print(elf_dead_exception)
        #print('Restarting with elf attack points %d' % (elf_ap + 1))
        elf_ap += 1
        continue # continue by reloading the grid and increased elf attack power

    # if no exception was caught and combat ended, we end up here - we found the right elf attack power
    else:
        ############# Combat has ended! ############
        # now determine the results
        # count hit points of remaining units
        total_hp = sum(u.get_hp() for u in units if u.isAlive())
        # determine which group won
        survivors = set(u.get_type() for u in units if u.isAlive())
        print('Combat ends after %d full rounds.' % rounds)
        print('Elf attack power is %d' % elf_ap)
        print('%s wins with total %d hitpoints remaining' % (survivors, total_hp))
        print('Outcome: %d * %d = %d' % (rounds, total_hp, rounds * total_hp))
        break