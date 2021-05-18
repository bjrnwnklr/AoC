import re
from itertools import combinations

text_weapons = """Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0
"""

text_armor = """Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
"""

text_rings = """Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""

class Player:
    def __init__(self, name, hp, d, a):
        self.name = name
        self.hp = hp
        self.d = d
        self.a = a

    def take_hit(self, damage):
        d_taken = max(1, damage - self.a)
        self.hp -= d_taken
        # print(f'{self.name} taking hit: {d_taken}. Remaining HP: {self.hp}')

    def is_alive(self):
        return self.hp > 0


def get_items(text):
    rpg_items = []
    regex = re.compile(r'\s(\d+)\b')
    for line in text.split('\n'):
        matches = regex.findall(line.strip())
        if matches:
            rpg_items.append((int(matches[0]), int(matches[1]), int(matches[2])))

    return rpg_items


def fight(player, enemy):
    combatants = [player, enemy]
    turn = 0
    while player.is_alive() and enemy.is_alive():
        # if turn is even, player attacks, otherwise enemy attacks
        attacker = combatants[turn % 2]
        attacked = combatants[(turn + 1) % 2]
        # print(f'Turn {turn}.')
        attacked.take_hit(attacker.d)
        turn += 1

    # someone has hp == 0, find out who
    if player.is_alive():
        return 'Player'
    else:
        return 'Enemy'


def player_wins(d, a):
    # calculate how many turns each combatant survives
    player_turns = 100 / max(1, 8 - a)
    enemy_turns = 104 / (d - 1)
    print(f'Player wins: {player_turns >= enemy_turns} P: {player_turns}, E: {enemy_turns}')

    return player_turns >= enemy_turns


if __name__ == '__main__':

    weapons = get_items(text_weapons)
    armor = get_items(text_armor)
    rings = get_items(text_rings)

    # add a 0 value ring and armor
    armor.append((0, 0, 0))
    rings.append((0, 0, 0))

    all_rings = list(combinations(rings, 1)) + list(combinations(rings, 2))

    results = []
    for w in weapons:
        for ar in armor:
            for r in all_rings:
                # calculate the value of the combined equipment
                cost = w[0] + ar[0] + sum(ring[0] for ring in r)
                # calculate player attributes
                damage = w[1] + sum(ring[1] for ring in r)
                defense = ar[2] + sum(ring[2] for ring in r)
                print(f'C: {cost}, W: {w}, Ar: {ar}, R: {r}')
                print(f'D: {damage}, A: {defense}')

                player = Player('Player', 100, damage, defense)
                enemy = Player('Enemy', 104, 8, 1)
                winner = fight(player, enemy)
                print(f'Winner: {winner}')
                results.append((cost, winner))
                # uncomment below for calculated solution, which is somehow wrong!
                # results.append((cost, player_wins(damage, defense)))

    # get the minimal cost
    part1 = min(rs[0] for rs in results if rs[1] == 'Player')
    # uncomment below for calculated solution, which is somehow wrong!
    # part1 = min(rs[0] for rs in results if rs[1])
    print(part1)

    # Part 1: 78
    # player = Player('Player', 100, 6, 3)
    # enemy = Player('Enemy', 104, 8, 1)
    # winner = fight(player, enemy)
    # print(winner)


