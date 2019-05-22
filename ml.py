import random
from collections import defaultdict

from keras.models import Sequential
from keras.layers import Dense
import numpy as np

from tic_tac_toe import TicTacToe


def default_factory():
    return {'total_reward': [0]*9, 'count': [0]*9}


states = defaultdict(default_factory)
for i in range(100000):
    data = []
    game = TicTacToe()
    while not game.is_ended():
        state = game.get_state()
        # print(state)
        player = game.current_player
        # print(player)
        valid_actions = [i for i, a in enumerate(game.get_valid_actions()) if a]
        action = random.choice(valid_actions)
        # print(action)
        game.take_action(action)
        data.append((player, state, action))
    score = game.get_score()

    for d in data:
        player, state, action = d
        action_score = score
        if player == 2:
            state = tuple(2 if s == 1 else 1 for s in state)
            action_score = -action_score
        states[state]['total_reward'][action] += action_score
        states[state]['count'][action] += 1

x_train = []
y_train = []
for state, reward in states.items():
    x_train.append(np.array(state))
    mean_reward = [reward['total_reward'][i]/(reward['count'][i]+1) for i in range(9)]
    y_train.append(np.array(mean_reward))


model = Sequential()

model.add(Dense(units=64, activation='relu', input_dim=9))
model.add(Dense(units=9, activation='softmax'))

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(np.array(x_train), np.array(y_train), epochs=1000, batch_size=32)

x_test = np.array([[1, 2, 0, 1, 2, 0, 0, 0, 0]])
y_test = model.predict(x_test, batch_size=1)
print(y_test)
