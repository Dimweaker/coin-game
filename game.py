from battle import Battle
from colorize import *
import bots
import emoji


class Game:
    def __init__(self, bots_list, bots_per_kind=2):
        self.bots_list = bots_list
        self.bots = []
        self.bots_per_kind = bots_per_kind
        self.total_coins = dict()
        self.matchmaking = set()

    def match(self, rounds_per_game=10):
        self.bots = [bot(number=str(i), rounds=rounds_per_game) for i in range(self.bots_per_kind) for bot in
                     self.bots_list]
        self.total_coins = {bot.name: 0 for bot in self.bots}
        for bot1 in self.bots:
            for bot2 in self.bots:
                if bot1.name != bot2.name and (bot2, bot1) not in self.matchmaking:
                    self.matchmaking.add((bot1, bot2))

    def play(self, rounds_per_game=10, games=50, verbose=True):
        for match in self.matchmaking:
            for i in range(games):
                battle = Battle(match[0], match[1], rounds_per_game)
                battle.combat(verbose=False)
                self.total_coins[match[0].name] += match[0].coins
                self.total_coins[match[1].name] += match[1].coins
                battle.reset()
        if verbose:
            self.show_result(rounds_per_game, games)

    def show_result(self, rounds_per_game=10, games=50):
        print(colorize(f'{"Final Result:":^28s}', 'red'))
        print(colorize(f'{"Rank":^6s}{"Player":^14s} {"Total Coins":^14s}', 'white'))
        sorted_bots = sorted(self.bots, key=lambda x: self.total_coins[x.name], reverse=True)
        for rank, bot in enumerate(sorted_bots):
            print(colorize(f'{rank + 1:^6d}', 'yellow'),
                  emoji.emojize(colorize(f'{bot.emoji}{bot.name:^12s}', 'blue')),
                  colorize(f'{self.total_coins[bot.name]:^12d}', "cyan"))
        print(colorize(f'Rounds per game: {rounds_per_game}', 'magenta'))
        print(colorize(f'Games per match: {games}', 'magenta'))
        print(colorize('Winner: ', 'green'), end='')
        print(colorize(max(self.total_coins, key=self.total_coins.get), 'green'))


if __name__ == '__main__':
    bots_list = [bots.Imitator, bots.Selfish, bots.Randomizer, bots.Nice, bots.Speculator, bots.Perception,
                 bots.Reverser,  bots.Why, bots.Holmes,  bots.Analyst, bots.Luck, bots.Compare, bots.Snobbish,
                 bots.Revenge, bots.Nico]
    game = Game(bots_list)
    game.match(rounds_per_game=10)
    game.play(rounds_per_game=10, games=100)
