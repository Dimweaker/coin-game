from battle import Battle
from colorize import *
import bots
import emoji


class Knockout:
    def __init__(self, bots_list, bots_per_kind=2):
        self.bots_list = bots_list
        self.bots = []
        self.bots_per_kind = bots_per_kind
        self.total_coins = dict()
        self.matchmaking = set()

    def generate_bot(self, rounds_per_game=10):
        self.bots = [bot(number=str(i), rounds=rounds_per_game) for i in range(self.bots_per_kind) for bot in
                     self.bots_list]

    def match(self):
        self.matchmaking = set()
        self.total_coins = {bot.name: 0 for bot in self.bots}
        for bot1 in self.bots:
            for bot2 in self.bots:
                if bot1.name != bot2.name and (bot2, bot1) not in self.matchmaking:
                    self.matchmaking.add((bot1, bot2))

    def play(self, rounds_per_game=10, when_to_show_ranks=10):
        self.match()
        i = 1
        while len(self.bots) > 1:
            for match in self.matchmaking:
                battle = Battle(match[0], match[1], rounds_per_game)
                battle.combat(verbose=False)
                self.total_coins[match[0].name] += match[0].coins
                self.total_coins[match[1].name] += match[1].coins
                battle.reset()
            print(colorize(f'Round{i}', 'magenta'), sep=' ')
            i += 1
            if len(self.bots) <= when_to_show_ranks:
                self.show_ranks()
            else:
                self.show_top()
            worst = min(self.bots, key=lambda x: self.total_coins[x.name])
            print(colorize(f'Out:', 'red'),
                  emoji.emojize(colorize(f'{worst.emoji}{worst.name:^14s}', 'blue')),
                  colorize(f'Coins: {self.total_coins[worst.name]:^14d}', 'cyan'))
            print('')
            self.bots.remove(worst)
        print(colorize(f'Winner:', 'red'),
              emoji.emojize(colorize(f'{self.bots[0].emoji}{self.bots[0].name:^14s}', 'blue')),
              colorize(f'Coins: {self.total_coins[self.bots[0].name]:^14d}', 'cyan'))

    def show_ranks(self):
        print(colorize(f'{"Ranks:"}', 'red'))
        print(colorize(f'{"Rank":^6s}{"Player":^14s} {"Total Coins":^14s}', 'white'))
        sorted_bots = sorted(self.bots, key=lambda x: self.total_coins[x.name], reverse=True)
        for rank, bot in enumerate(sorted_bots):
            print(colorize(f'{rank + 1:^6d}', 'yellow'),
                  emoji.emojize(colorize(f'{bot.emoji}{bot.name:^12s}', 'blue')),
                  colorize(f'{self.total_coins[bot.name]:^12d}', "cyan"))

    def show_top(self, number=3):
        print(colorize(f'{f"TOP{number}:"}', 'red'))
        print(colorize(f'{"Rank":^6s}{"Player":^14s} {"Total Coins":^14s}', 'white'))
        sorted_bots = sorted(self.bots, key=lambda x: self.total_coins[x.name], reverse=True)[:number]
        for rank, bot in enumerate(sorted_bots):
            print(colorize(f'{rank + 1:^6d}', 'yellow'),
                  emoji.emojize(colorize(f'{bot.emoji}{bot.name:^12s}', 'blue')),
                  colorize(f'{self.total_coins[bot.name]:^12d}', "cyan"))


if __name__ == '__main__':
    bots_list = [bots.Imitator, bots.Selfish, bots.Randomizer, bots.Nice, bots.Speculator, bots.Perception,
                 bots.Reverser, bots.Why, bots.Holmes, bots.Analyst, bots.Luck, bots.Compare, bots.Snobbish,
                 bots.Revenge, bots.Nico]
    game = Knockout(bots_list)
    game.generate_bot(rounds_per_game=10)
    game.play(rounds_per_game=10)
