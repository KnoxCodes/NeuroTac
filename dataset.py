import numpy as np
from game import TicTacToe
from teacher import teacher_move

def generate_dataset(num_games=30000):
    X, y = [], []

    for _ in range(num_games):
        game = TicTacToe()
        player = 1

        while True:
            move = teacher_move(game, player)
            X.append(game.board.copy())
            y.append(move)

            game.make_move(move, player)
            winner = game.check_winner()
            if winner is not None:
                break
            player *= -1

    return np.array(X), np.array(y)