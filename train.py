import numpy as np
import torch
import torch.nn as nn
import random
from network import DQN
import bots
from battle import Battle
import random

bots_list = [bots.Imitator, bots.Selfish, bots.Randomizer, bots.Nice, bots.Speculator, bots.Perception,
             bots.Reverser, bots.Why, bots.Holmes, bots.Analyst, bots.Luck, bots.Compare, bots.Snobbish,
             bots.Revenge, bots.Nico]


class Rocket(bots.Bot):
    def __init__(self, model, name="Rocket", emoji=":rocket:", number='', rounds=10):
        super().__init__(name + number, rounds=10, emoji=emoji)
        self.model = model
        self.flag = 0

    def action(self):
        actions = [1, -1]
        if self.flag:
            record = torch.from_numpy(np.array(self.record)).float()
            if torch.cuda.is_available():
                record = record.cuda()
            index = self.model(record).argmax()
            return actions[index]
        else:
            return random.choice(actions)


def train():
    if torch.cuda.is_available():
        torch.cuda.manual_seed(123)
    else:
        torch.manual_seed(123)

    model = DQN()
    replay_memory = []

    if torch.cuda.is_available():
        model.cuda()

    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
    criterion = nn.MSELoss()

    ai_bot = Rocket(model)
    battle_list = [Battle(ai_bot, opponent_bot()) for opponent_bot in bots_list]

    battle = random.choice(battle_list)
    state = torch.from_numpy(np.array(battle.record)).float()

    initial_epsilon = 0.2
    target_epsilon = 0.001
    batch_size = 128
    replay_memory_size = 20000
    gamma = 0.99

    for i in range(100000):
        epsilon = max(initial_epsilon * (0.999 ** i), target_epsilon)
        if random.random() < epsilon:
            battle.bot1.flag = 0
        else:
            battle.bot1.flag = 1

        turns = battle.get_turns()
        reward, _ = battle.battle_by_steps()
        next_state = torch.from_numpy(np.array(battle.record)).float()
        if torch.cuda.is_available():
            state = state.cuda()
            next_state = next_state.cuda()
        action = battle.record[0][turns]
        replay_memory.append((state, action, reward, next_state, turns))

        if len(replay_memory) > replay_memory_size:
            del replay_memory[0]

        batch = random.sample(replay_memory, min(len(replay_memory), batch_size))
        state_batch, action_batch, reward_batch, next_state_batch, turns_batch = zip(*batch)
        state_batch = torch.cat(state_batch)
        next_state_batch = torch.cat(next_state_batch)
        action_batch = torch.from_numpy(
            np.array([[1, 0] if action == 1 else [0, 1] for action in action_batch], dtype=np.float32))
        reward_batch = torch.from_numpy(np.array(reward_batch, dtype=np.float32)[:, None])

        if torch.cuda.is_available():
            action_batch = action_batch.cuda()
            reward_batch = reward_batch.cuda()
            state_batch = state_batch.cuda()
            next_state_batch = next_state_batch.cuda()

        current_prediction_batch = model(state_batch)
        next_prediction_batch = model(next_state_batch)

        y = tuple(reward if turn == 9 else reward + gamma * torch.max(prediction) for reward, turn, prediction in
                  zip(reward_batch, turns_batch, next_prediction_batch))
        y_batch = torch.cat(y)

        q_value = torch.sum(current_prediction_batch * action_batch, dim=1)
        optimizer.zero_grad()
        loss = criterion(q_value, y_batch)
        loss.backward()
        optimizer.step()

        if turns == 9:
            battle.reset()
            battle = random.choice(battle_list)
            state = torch.from_numpy(np.array(battle.record)).float()
        else:
            state = next_state

        if i % 100 == 0:
            print("Episode: {}, Loss: {}, Epsilon: {}".format(i, loss, epsilon))

        if i % 10000 == 0:
            torch.save(model, f"model_{i}.pth")

    torch.save(model, "model.pth")


if __name__ == '__main__':
    train()
