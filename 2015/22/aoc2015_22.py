

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

        # print(f'{self.name} taking hit: {d_taken}. Remaining HP: {self.hp}')

    def is_alive(self):
        return self.hp > 0




class Fight:
    def __init__(self):
        self.player_hp = 50
        self.player_mana = 500
        self.player_armor = 0
        self.player_mana_consumption = 0
        self.player_magic_armor = 0
        self.enemy_hp = 51
        self.enemy_d = 9
        self.effects = {
            'sh': 0, # shield
            'po': 0, # poison
            're': 0  # recharge
        }

    def hashcode(self):
        return hash(self)

    def __repr__(self):
        return ','.join(str(x) for x in [
            self.player_hp,
            self.player_mana,
            self.player_armor,
            self.player_mana_consumption,
            self.player_magic_armor,
            self.enemy_hp,
            self.enemy_d,
            self.effects['sh'],
            self.effects['po'],
            self.effects['re']
        ])

    def hit_enemy(self, d):
        self.enemy_hp -= d

    def hit_player(self, d):
        self.player_hp -= max(1, d - self.player_armor - self.player_magic_armor)

    def update_effects(self):
        # shield effect
        if self.effects['sh'] > 0:
            self.player_magic_armor = 7
            self.effects['sh'] -= 1
        else:
            self.player_magic_armor = 0
        # poison effect
        if self.effects['po'] > 0:
            # self.enemy.take_hit(3)
            self.effects['po'] -= 1
        # recharge effect
        if self.effects['re'] > 0:
            self.player_mana += 101
            self.effects['re'] -= 1








if __name__ == '__main__':

    new_round = Fight()
    print(f'{new_round}')
    print(f'{new_round.hashcode()}')



