import timeit
from collections import deque

# f_name = 'ex1.txt'
f_name = 'input.txt'


def print_decks(players):
    for p in players:
        print(f"Player {p}'s deck: {players[p]}")


def play_recursive(players):
    global total_games

    total_games += 1
    game = total_games
    # print()
    # print(f'=== Game {game} ===')

    configs = []

    rounds = 0
    winner = 0
    while all(players.values()):
        # check if we had the same config previously
        current_config = [tuple(players[p]) for p in players]
        if current_config in configs:
            winner = 0
            # print(f'Recursion prevention! The winner of game {game} is player {winner}!')
            return winner
        else:

            # add current decks to configs
            configs.append(current_config)

            rounds += 1
            # print()
            # print(f'-- Round {rounds} (Game {game}) --')
            # print_decks(players)

            cards = []
            for p in players:
                card = players[p].popleft()
                # print(f'Player {p} plays: {card}')
                cards.append(card)

            # check for recursive game!
            if all(len(players[p]) >= cards[p] for p in players):
                # print('Playing a sub-game to determine the winner...')
                next_players = {
                    p: deque(list(players[p])[:cards[p]])
                    for p in players
                }
                winner = play_recursive(next_players)
                # print()
                # print(f'...anyway, back to game {game}.')
            else:
                winner = 0 if cards[0] > cards[1] else 1

            # print(f'Player {winner} wins round {rounds} of game {game}!')
            # add cards to bottom of winner's stack
            players[winner].extend([cards[winner], cards[(winner + 1) % 2]])

    # Winner of the game
    # print(f'The winner of game {game} is player {winner}!')
    return winner


if __name__ == '__main__':
    players = dict()
    with open(f_name, 'r') as f:
        stacks = f.read().split('\n\n')
        for player, s in enumerate(stacks):
            cards = s.strip().split('\n')[1:]
            players[player] = deque([int(c.strip()) for c in cards])

    # Play!
    start_time = timeit.default_timer()
    total_games = 0
    winner = play_recursive(players)
    print(f'Duration: {timeit.default_timer() - start_time:.2f} seconds')
    print()
    print('== Post-game results ==')
    print_decks(players)

    # Calculate the winning player's score:
    mult = lambda x: x[0] * x[1]
    score = sum(map(mult, zip(range(len(players[winner]), 0, -1), players[winner])))
    print(f'Winning score: {score}')

    # part 1: 31957 (player 0 - the crab! - wins!)
    # part 2: 33212 (player 0 - the crab! - wins!)
