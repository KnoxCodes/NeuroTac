import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros(9)

    def reset(self):
        self.board = np.zeros(9)

    def available_moves(self):
        return [i for i in range(9) if self.board[i] == 0]

    def make_move(self, pos, player):
        if self.board[pos] == 0:
            self.board[pos] = player
            return True
        return False

    def check_winner(self):
        lines = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for line in lines:
            s = sum(self.board[line])
            if s == 3: return 1
            if s == -3: return -1
        if 0 not in self.board:
            return 0
        return None