from copy import deepcopy
from heapq import heappush, heappop

spells = {
    'mm': 53,
    'dr': 73,
    'sh': 113,
    'po': 173,
    're': 229
}


class Fight:
    def __init__(self):
        self.player_hp = 50
        self.player_mana = 500
        self.player_armor = 0
        self.player_mana_consumed = 0
        self.player_magic_armor = 0
        self.enemy_hp = 51
        self.enemy_d = 9
        self.effects = {
            'sh': 0,  # shield
            'po': 0,  # poison
            're': 0  # recharge
        }

        self.turn = 0
        self.winner = None

    def hashcode(self):
        return hash(self)

    def __repr__(self):
        return ','.join(str(x) for x in [
            self.player_hp,
            self.player_mana,
            self.player_armor,
            self.player_mana_consumed,
            self.player_magic_armor,
            self.enemy_hp,
            self.enemy_d,
            self.effects['sh'],
            self.effects['po'],
            self.effects['re']
        ])

    def __lt__(self, other):
        return self.hashcode() < other.hashcode()

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
            self.hit_enemy(3)
            self.effects['po'] -= 1
        # recharge effect
        if self.effects['re'] > 0:
            self.player_mana += 101
            self.effects['re'] -= 1

    def player_wins(self):
        return self.player_hp > 0 and self.enemy_hp <= 0

    def enemy_wins(self):
        return self.player_hp <= 0 and self.enemy_hp > 0

    def get_possible_spells(self):
        # return a list of possible spells
        poss_spells = []
        for sp in spells:
            if self.player_mana >= spells[sp] and (sp not in self.effects or self.effects[sp] <= 1):
                poss_spells.append(sp)
        return poss_spells

    def fight_round(self, spell):
        # for part 2, reduce mana by 1 with each turn
        if part == 2:
            self.player_hp -= 1
            if self.enemy_wins():
                self.winner = 'Enemy'
                return True

        # --- Player's turn ---
        # apply effects
        self.update_effects()
        # check if player has won (if enemy was killed by an effect like poison)
        if self.player_wins():
            self.winner = 'Player'
            return True

        # run player attack: cast a spell
        if spell == 'mm':
            self.hit_enemy(4)
        elif spell == 'dr':
            self.hit_enemy(2)
            self.player_hp += 2
        elif spell == 'sh':
            self.effects[spell] = 6
        elif spell == 'po':
            self.effects[spell] = 6
        elif spell == 're':
            self.effects[spell] = 5
        # update mana and consumption with the mana used
        self.player_mana -= spells[spell]
        self.player_mana_consumed += spells[spell]

        # check if player has won
        if self.player_wins():
            self.winner = 'Player'
            return True

        # --- Enemy's turn ---
        # apply effects and check if player has won
        self.update_effects()
        if self.player_wins():
            self.winner = 'Player'
            return True
        # run enemy attack
        self.hit_player(self.enemy_d)
        if self.enemy_wins():
            self.winner = 'Enemy'
            return True



if __name__ == '__main__':
    part = 2
    new_round = Fight()

    # Dijkstra
    # seen = set()
    # q = [(0, new_round)]
    # while q:
    #     (cost, curr_round) = heappop(q)
    #     if curr_round.hashcode() not in seen:
    #         seen.add(curr_round.hashcode())
    #         if curr_round.winner == 'Player':
    #             print(f'Player wins, mana consumed: {curr_round.player_mana_consumed}')
    #             break
    #
    #         for spell in curr_round.get_possible_spells():
    #             next_round = deepcopy(curr_round)
    #             next_round.fight_round(spell)
    #             if next_round.winner != 'Enemy':
    #                 heappush(q, (next_round.player_mana_consumed, next_round))
    #
    # print('Bla')

    # no Dijkstra, just run through every scenario and record who wins with how much mana consumed
    q = [new_round]
    results = []
    while q:
        curr_round = q.pop()
        for spell in curr_round.get_possible_spells():
            next_round = deepcopy(curr_round)
            next_round.fight_round(spell)
            # print(spell, next_round)
            if next_round.winner is not None:
                results.append((next_round.winner, next_round.player_mana_consumed))
                print(f'Winner: {next_round.winner}, {next_round.player_mana_consumed}, {next_round}')
            else:
                q.append(next_round)

    # Part 1: 900 (logged all results to a file and filtered for winner=='Player' and lowest Mana consumed was 900
    # Part 2: 1216 (same- runs for a long time!)

    # Implement pruning: prune any paths that have higher mana consumption than the lowest Player winning path.
    