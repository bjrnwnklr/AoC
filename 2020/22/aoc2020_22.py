# f_name = 'ex1.txt'
f_name = 'input.txt'


def print_decks():
    for p in players:
        print(f"Player {p}'s deck: {players[p]}")


players = dict()
with open(f_name, 'r') as f:
    stacks = f.read().split('\n\n')
    for player, s in enumerate(stacks):
        cards = s.strip().split('\n')[1:]
        players[player] = [int(c.strip()) for c in cards]

# Play!
rounds = 0
winner = 0
while all(players.values()):
    rounds += 1
    print(f'-- Round {rounds} --')
    print_decks()

    cards = []
    for p in players:
        card = players[p].pop(0)
        print(f'Player {p} plays: {card}')
        cards.append(card)

    winner = 0 if cards[0] > cards[1] else 1
    print(f'Player {winner} wins the round!')

    # add cards to bottom of winner's stack
    players[winner].extend(sorted(cards, reverse=True))
    print()

print()
print('== Post-game results ==')
print_decks()

# Calculate the winning player's score:
mult = lambda x: x[0] * x[1]
score = sum(map(mult, zip(range(len(players[winner]), 0, -1), players[winner])))
print(f'Winning score: {score}')

# part 1: 31957 (player 0 - the crab! - wins!)


