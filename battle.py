import bots
import emoji
from colorize import *


class Battle:
    def __init__(self, bot1, bot2, rounds=10):
        self.bot1 = bot1
        self.bot2 = bot2
        self.record = [[0 for _ in range(rounds)], [0 for _ in range(rounds)]]
        self.rounds = rounds

    def combat(self, verbose=True):
        self.record = [[0 for _ in range(self.rounds)], [0 for _ in range(self.rounds)]]
        for i in range(self.rounds):
            coins1 = self.bot1.player_coins
            coins2 = self.bot2.player_coins
            action1 = self.bot1.action()
            action2 = self.bot2.action()
            self.record[0][i] = action1
            self.record[1][i] = action2
            self.bot1.record = self.record
            self.bot2.record = self.record[::-1]
            self.bot1.coins = self.bot1.player_coins
            self.bot2.coins = self.bot2.player_coins
            coins_change1 = self.bot1.player_coins - coins1
            coins_change2 = self.bot2.player_coins - coins2
            if verbose:
                print(colorize(f'Round {i + 1}:', 'red'))
                print(
                    colorize(f'{"  Player":^12s} {"Coins":^5s} {"Action":^10s} {"Change":^6s} {"Coins":^7s}', 'white'))
                print(emoji.emojize(colorize(f'{self.bot1.emoji}{self.bot1.name:^10s}', 'blue')),
                      colorize(f'{coins1:^5d}', "cyan"),
                      colorize(f'{bots.actions_dict[action1]:^10s}', "magenta" if action1 == 1 else "yellow"),
                      colorize(f'{coins_change1:+3d}', "green" if coins_change1 > 0 else "red"),
                      colorize(f'{self.bot1.coins:6d}', "cyan"))
                print(emoji.emojize(colorize(f'{self.bot2.emoji}{self.bot2.name:^10s}', 'blue')),
                      colorize(f'{coins2:^5d}', "cyan"),
                      colorize(f'{bots.actions_dict[action2]:^10s}', "magenta" if action2 == 1 else "yellow"),
                      colorize(f'{coins_change2:+3d}', "green" if coins_change2 > 0 else "red"),
                      colorize(f'{self.bot2.coins:6d}', "cyan"))
                print('----------------------------------')
                input('Press Enter to continue...')
        if verbose:
            print(colorize(f'{"Final Result:":^20s}', 'red'))
            print(colorize(f'{"Player":^12s} {"Coins":^5s}', 'white'))
            print(emoji.emojize(colorize(f'{self.bot1.emoji}{self.bot1.name:^10s}', 'blue')),
                  colorize(f'{self.bot1.coins:^5d}', "cyan"))
            print(emoji.emojize(colorize(f'{self.bot2.emoji}{self.bot2.name:^10s}', 'blue')),
                  colorize(f'{self.bot2.coins:^5d}', "cyan"))
            print('----------------------------------')
            print('')

    def battle_by_steps(self):
        i = self.get_turns()
        coins1 = self.bot1.player_coins
        coins2 = self.bot2.player_coins
        action1 = self.bot1.action()
        action2 = self.bot2.action()
        self.record[0][i] = action1
        self.record[1][i] = action2
        self.bot1.record = self.record
        self.bot2.record = self.record[::-1]
        self.bot1.coins = self.bot1.player_coins
        self.bot2.coins = self.bot2.player_coins
        coins_change1 = self.bot1.player_coins - coins1
        coins_change2 = self.bot2.player_coins - coins2
        return coins_change1, coins_change2

    def reset(self):
        self.bot1.reset()
        self.bot2.reset()
        self.record = [[0 for _ in range(self.rounds)], [0 for _ in range(self.rounds)]]

    def get_turns(self) -> int:
        return self.record[0].index(0)


if __name__ == '__main__':
    battle = Battle(bots.Randomizer(), bots.Rocket())
    battle.combat()
