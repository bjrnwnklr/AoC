import re


class Army():
    def __init__(self, group, id, units, hp, dmg, initiative, at_type, immune, weak):
        self.group = group
        self.id = id
        self.units = units
        self.hp = hp
        self.dmg = dmg
        self.at_type = at_type
        self.initiative = initiative
        self.immune = immune
        self.weak = weak

    def __str__(self):
        s = 'Group: %s; ID: %d; units: %d; hp: %d; dmg: %d; at_type: %s; init: %d' % (self.group, self.id, self.units, self.hp, self.dmg, self.at_type, self.initiative)
        s += '\n\tImmune: %s; Weak: %s' % (str(self.immune), str(self.weak))  
        return s

    def power(self):
        return self.units * self.dmg

    def estimate_damage_from(self, enemy):
        """
        return how much damage this army will take from an enemy
        """
        if enemy.at_type in self.immune:
            return 0
        elif enemy.at_type in self.weak:
            return enemy.power() * 2
        else:
            return enemy.power()

    def take_damage_from(self, enemy):
        """
        take damage from an enemy and set alive status to dead if no units left
        """
        if enemy.at_type in self.immune:
            damage_taken = 0
        elif enemy.at_type in self.weak:
            damage_taken = enemy.power() * 2
        else:
            damage_taken = enemy.power()

        killed = min(self.units, damage_taken // self.hp)
        self.units -= killed


       # print('%s group %d deals %d damage to %s group %d, killing %d units. %d units left' %
        #        (enemy.group, enemy.id, damage_taken, self.group, self.id, killed, self.units))



############ helper functions ##############

def extract_input(unit_group, input_string):
    re_search_digits = re.compile(r'(\d+)')
    re_search_immune = re.compile(r'immune to (\w+([\s,]*\w+)*)[;\)]')
    re_search_weak = re.compile(r'weak to (\w+([\s,]*\w+)*)[;\)]')
    re_search_at_type = re.compile(r'(\w+) damage')

    army = []

    for i, l in enumerate(input_string.split('\n')[1:]):
        immune, weak = [], []

        results_digits = re.findall(re_search_digits, l)
        if results_digits:
            units, hp, dmg, initiative = map(int, results_digits)

        results_immunity = re.search(re_search_immune, l)
        if results_immunity:
            immune = results_immunity.group(1).split(', ')

        results_weak = re.search(re_search_weak, l)
        if results_weak:
            weak = results_weak.group(1).split(', ')

        results_at_type = re.search(re_search_at_type, l)
        if results_at_type:
            at_type = results_at_type.group(1)

        #a = Army(unit_group, i + 1, units, hp, dmg, initiative, at_type, immune, weak)
        a = [unit_group, i + 1, units, hp, dmg, initiative, at_type, immune, weak]
        army.append(a)
    
    return army




############# MAIN #############



def battle(immunes, infection):
    
    prev_unit_count = 10000000
    
    # FIGHT!
    while immunes and infection:
        all_armies = immunes + infection

        selection = dict()
        chosen = set()

        # sort by effective power and initiative
        armies = sorted([u for u in all_armies if u.units > 0], key = lambda x: (-x.power(), -x.initiative))
        for x in armies:
            to_attack = sorted([u for u in armies
                                if u.group != x.group
                                and u not in chosen
                                and u.estimate_damage_from(x) > 0], 
                    key = lambda z: (-z.estimate_damage_from(x), -z.power(), -z.initiative))
            if to_attack:
                if to_attack[0] not in chosen:
                    selection[x] = to_attack[0]
                    chosen.add(to_attack[0])
                    #print('%s unit %d selects %s unit %d' % (x.group, x.id, to_attack[0].group, to_attack[0].id))

        #print('\n')
        for x in sorted(armies, key = lambda z: -z.initiative):
            if x in selection:
                selection[x].take_damage_from(x)

        #print('\n')
        immunes = [x for x in immunes if x.units > 0]
        infection = [x for x in infection if x.units > 0]

        # determine the winner and check if any units were killed this round
        immune_left = sum(x.units for x in immunes)
        infection_left = sum(x.units for x in infection)

        unit_count = immune_left + infection_left
        if unit_count == prev_unit_count:
            return 'Infection', infection_left
        else:
            prev_unit_count = unit_count

        if infection_left == 0:
            return 'Immune', immune_left
        elif immune_left == 0:
            return 'Infection', infection_left

if __name__ == '__main__':
    f = open(r'input.txt', 'r')
    immune_f, infection_f = f.read().split('\n\n')
    f.close()

    raw_immunes = extract_input('immune', immune_f)
    raw_infection = extract_input('infection', infection_f)

    immunes = []
    infection = []
    # create army
    for a in raw_immunes:
        immunes.append(Army(*a))

    for a in raw_infection:
        infection.append(Army(*a))

    # FIGHT!
    winner, units_left = battle(immunes, infection) 
    print('Part 1: %s wins with %d units left\n\n\n' % (winner, units_left))

    
    # run through boost increases (should probably do binary search...)
    boost = 1
    found = False
    while not found:
        immunes = []
        infection = []
        # create army and increase boost for immunes
        for a in raw_immunes:
            a_copy = a[:]
            a_copy[4] += boost
            immunes.append(Army(*a_copy))

        for a in raw_infection:
            infection.append(Army(*a))

        winner, units_left = battle(immunes, infection)
        if winner == 'Immune':
            print('Boost found: %d' % boost)
            print('%s wins with %d units left' % (winner, units_left))
            found == True
            break
        else:
            print('---- :( Boost %d not enough' % boost)
            boost += 1
    