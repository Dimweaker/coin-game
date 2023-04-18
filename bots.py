import random


actions_dict = {1: 'cooperate🤝', -1: 'defect👊', 0: 'wait'}


class Bot:
    def __init__(self, name, emoji=':robot:', rounds=10):
        self.name = name
        self.emoji = emoji
        self.rounds = rounds
        self.record = [[0 for _ in range(rounds)], [0 for _ in range(rounds)]]
        self.coins = rounds

    def get_turns(self) -> int:
        """
        Get the number of turns that have passed
        获取已经过去的回合数
        """
        return self.record[0].index(0)

    def get_player_coins(self) -> int:
        """
        Get the number of coins the player has
        获取玩家拥有的金币数
        """
        return 10 - self.record[0].count(1) + self.record[1].count(1) * 3

    def get_opponent_coins(self) -> int:
        """
        Get the number of coins the opponent has
        获取对手拥有的金币数
        """
        return self.rounds - self.record[1].count(1) + self.record[0].count(1) * 3

    def reset(self):
        """
        Reset the record of the game
        重置游戏记录
        """
        if 0 not in self.record[0]:
            self.record = [[0 for _ in range(self.rounds)], [0 for _ in range(self.rounds)]]
            self.coins = self.rounds


class Imitator(Bot):
    """
    Imitates the opponent's last move
    模仿对手的最后一次行动
    """
    def __init__(self, name="Imitator", number='', rounds=10):
        super().__init__(name + number, rounds=rounds)

    def action(self) -> int:
        if self.get_turns() == 0:
            return 1
        else:
            return self.record[1][self.get_turns() - 1]


class Randomizer(Bot):
    """
    Randomly chooses to cooperate or defect
    随机选择合作或欺骗
    """
    def __init__(self, name="Randomizer", number='', rounds=10):
        super().__init__(name + number, rounds=rounds)

    def action(self) -> int:
        r = random.random()
        if r < 0.5:
            return 1
        else:
            return -1


class Selfish(Bot):
    """
    Always defects
    总是欺骗
    """
    def __init__(self, name="Selfish", number='', rounds=10):
        super().__init__(name + number, rounds=rounds)

    def action(self) -> int:
        return -1


class Nice(Bot):
    """
    Always cooperates
    总是合作
    """
    def __init__(self, name="Nice", number='', rounds=10):
        super().__init__(name + number, rounds=rounds)

    def action(self) -> int:
        return 1


class Speculator(Bot):
    """
    Cooperates until the opponent defects, then defects
    选择合作直到对手选择欺骗，然后欺骗
    """
    def __init__(self, name="Speculator", number='', rounds=10):
        super().__init__(name + number, rounds=rounds)

    def action(self) -> int:
        if self.get_turns() == 0:
            return 1
        elif -1 in self.record[1]:
            return -1
        else:
            return 1


class Perception(Bot):
    """
    Choose by the opponent's first move
    根据对手的第一次行动选择
    """
    def __init__(self, name="Perception", number='', rounds=10):
        super().__init__(name + number, rounds=rounds)

    def action(self) -> int:
        if self.get_turns() == 0:
            return 1
        else:
            return self.record[1][0]


class Reverser(Bot):
    """
    Choose the opposite of the opponent's last move
    选择与对手的最后一次行动相反的行动
    """
    def __init__(self, name="Reverser", number='', rounds=10):
        super().__init__(name + number, rounds=rounds)

    def action(self) -> int:
        if self.get_turns() == 0:
            return 1
        else:
            return -self.record[1][self.get_turns() - 1]


class Merlin(Bot):
    """
    Cooperates if coins are more than 10, defects otherwise
    金币数大于等于10时合作，否则欺骗
    """

    def __init__(self, name="Merlin", number='', emoji=":grinning_face:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)

    def action(self) -> int:
        if self.get_player_coins() >= 10:
            return 1
        else:
            return -1


class Why(Bot):
    """
    Choose by trust value
    根据信任值选择
    """
    def __init__(self, name="JB114514CM", number='', emoji=":face_without_mouth:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)

    def action(self) -> int:
        if self.get_turns() == 0:
            return 1
        else:
            return self.record[1][0]

    def get_trust(self) -> int:
        """
        Get the trust value of the opponent
        获取对手的信任值
        """
        trust = 1
        turns = self.get_turns()
        if turns == 0:
            return 1
        else:
            if self.record[turns-1][1] == -1:
                trust -= 1
            else:
                if self.record[turns-1][0] == -1:
                    trust += 2
                else:
                    trust += 1
        return 1 if trust > 0 else -1


class Holmes(Bot):
    """
    Imitates the opponent's last move if opponent defects less than 2 times, otherwise defects
    如果对手欺骗次数小于2次，模仿对手的最后一次行动，否则欺骗
    """
    def __init__(self, name="Holmes", number='', emoji=":detective:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)

    def action(self) -> int:
        if self.get_turns() == 0:
            return 1
        else:
            if self.record[1].count(-1) < 2:
                return self.record[1][self.get_turns() - 1]
            else:
                return -1


class White(Bot):
    """
    If opponent cooperates, choose to cooperate 2 times, otherwise choose to defect
    如果对手合作，选择合作2次，否则选择欺骗
    """
    def __init__(self, name="White", number='', emoji=":face_blowing_a_kiss:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)

    def action(self) -> int:
        turns = self.get_turns()
        if turns == 0:
            return 1
        elif turns == 1:
            return self.record[1][0]
        else:
            if 1 in self.record[1][turns-2:turns]:
                return 1
            else:
                return -1


class Planner(Bot):
    """
    Cooperates two times and defects one times;if opponent defects more than 2 times, defects
    选择合作1次，欺骗1次；如果对手欺骗次数大于等于2次，选择欺骗
    """
    def __init__(self, name="Planner", number='', emoji=":face_with_monocle:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)

    def action(self) -> int:
        turns = self.get_turns()
        if self.record[1].count(-1) >= 2:
            return -1
        else:
            return 1 if turns % 2 == 0 else -1


class Luck(Bot):
    """
    If opponent detects odd number of times, defects, otherwise cooperates
    如果对手欺骗奇数次，选择欺骗，否则选择合作
    """
    def __init__(self, name="Dululu", number='', emoji=":zany_face:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)

    def action(self) -> int:
        return 1 if self.record[1].count(-1) % 2 == 0 else -1


class Revenge(Bot):
    """
    If opponent defects, choose to defect 2 times, otherwise choose to cooperate
    如果对手欺骗，选择欺骗2次，否则选择合作
    """
    def __init__(self, name="M0nesy", number='', emoji=":smiling_face_with_smiling_eyes:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)

    def action(self) -> int:
        turns = self.get_turns()
        if turns == 0:
            return 1
        elif turns == 1:
            return self.record[1][0]
        else:
            if -1 in self.record[1][turns-2:turns]:
                return -1
            else:
                return 1


class Compare(Bot):
    """
    Defect if opponent's coins are more than mine, otherwise cooperate
    如果对手金币数大于我的金币数，选择欺骗，否则选择合作
    """
    def __init__(self, name="SDDL", number='', emoji=":bear:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)

    def action(self) -> int:
        if self.get_player_coins() < self.get_opponent_coins():
            return -1
        else:
            return 1


class Snobbish(Bot):
    """
    Defect if opponent's coins are less than mine, otherwise cooperate
    如果对手金币数小于我的金币数，选择欺骗，否则选择合作
    """
    def __init__(self, name="LDDS", number='', emoji=":teddy_bear:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)

    def action(self) -> int:
        if self.get_player_coins() > self.get_opponent_coins():
            return -1
        else:
            return 1


class Nico(Bot):
    """
    Cooperate in the first 4 rounds, if coins more than 10 in the first 5 rounds, cooperate in the next 5 rounds;otherwise defect
    前五轮合作；如果第四轮后硬币大于10，则之后一直合作，否则一直欺骗
    """
    def __init__(self, name="Nico", number='', emoji=":smiling_face:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)
        self.flag = 0

    def action(self) -> int:
        turns = self.get_turns()
        if turns < 4:
            self.flag = 0
            return 1
        elif turns == 4:
            self.flag = self.get_player_coins() > 10
            return 1 if self.flag else -1
        else:
            return 1 if self.flag else -1


class Analyst(Bot):
    """
    If opponent's cooperation ratio is greater than 0.5, cooperate, otherwise defect
    如果对方合作的比例大于0.5，选择合作，否则选择欺骗
    """
    def __init__(self, name="Analyst", number='', emoji=":face_with_hand_over_mouth:", rounds=10):
        super().__init__(name + number, emoji=emoji, rounds=rounds)

    def action(self) -> int:
        if self.get_turns() == 0:
            return 1
        else:
            return 1 if self.record[1].count(1) / self.get_turns() > 0.6 else -1
