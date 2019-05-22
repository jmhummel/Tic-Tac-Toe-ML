from typing import List


class TicTacToe:
    def __init__(self):
        self.state = [0] * 9
        self.turn = 1
        self.current_player = 1

    def get_action_size(self):
        return 9

    def get_valid_actions(self):
        return tuple(1 if square == 0 else 0 for square in self.state)

    def get_state(self):
        return tuple(self.state)

    def take_action(self, action):
        self.state[action] = self.current_player
        self.current_player = 2 if self.current_player == 1 else 1

    def check_squares(self, indexes: List[int]) -> int or None:
        mark = self.state[indexes[0]]
        for i in indexes[1:]:
            if mark != self.state[i]:
                return None
        return mark

    def is_draw(self):
        for square in self.state:
            if square == 0:
                return False
        return True

    def is_ended(self):
        return self.get_winner() or self.is_draw()

    def get_winner(self):
        for indexes in [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]:
            winner = self.check_squares(indexes)
            if winner:
                return winner
        return None

    def get_score(self):
        winner = self.get_winner()
        if winner == 1:
            return 1
        elif winner == 2:
            return -1
        return 0

