import re
from itertools import combinations
from math import ceil


spells = {
    'mm': 53,
    'dr': 73,
    'sh': 113,
    'po': 173,
    're': 229
}


class Player:
    def __init__(self, name, hp, d, a, mana):
        self.name = name
        self.hp = hp
        self.d = d
        self.a = a
        self.mana = mana
        self.magic_armor = 0

    def take_hit(self, damage):
        d_taken = max(1, damage - self.a - self.magic_armor)
        self.hp -= d_taken
        # print(f'{self.name} taking hit: {d_taken}. Remaining HP: {self.hp}')

    def is_alive(self):
        return self.hp > 0




class Fight:
    def __init__(self, player, enemy):
        self.effects = {
            'sh': 0, # shield
            'po': 0, # poison
            're': 0  # recharge
        }
        self.player = player
        self.enemy = enemy

    def fight(self):
        turn = 0
        while self.player.is_alive() and self.enemy.is_alive():
            # apply impacts of effects
            self.update_effects()

            # Player's turn
            # pick a spell


            # print(f'Turn {turn}.')
            attacked.take_hit(attacker.d)

        # someone has hp == 0, find out who
        if self.player.is_alive():
            return 'Player'
        else:
            return 'Enemy'

    def update_effects(self):
        # shield effect
        if self.effects['sh'] > 0:
            self.player.magic_armor = 7
            self.effects['sh'] -= 1
        else:
            self.player.magic_armor = 0
        # poison effect
        if self.effects['po'] > 0:
            self.enemy.take_hit(3)
            self.effects['po'] -= 1
        # recharge effect
        if self.effects['re'] > 0:
            self.player.mana += 101
            self.effects['re'] -= 1








if __name__ == '__main__':

    player = Player()

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

    # get the minimal cost
    part1 = min(rs[0] for rs in results if rs[1] == 'Player')
    print(part1)




