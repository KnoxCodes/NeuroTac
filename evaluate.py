import torch
from game import TicTacToe
from teacher import teacher_move

def model_move(model, game):
    with torch.no_grad():
        board = torch.FloatTensor(game.board).unsqueeze(0)
        logits = model(board)
        probs = torch.softmax(logits, dim=1)[0]

    valid_moves = game.available_moves()
    best_move = max(valid_moves, key=lambda x: probs[x].item())
    return best_move

def evaluate(model, opponent="random", games=1000):
    wins, losses, draws = 0,0,0

    for _ in range(games):
        game = TicTacToe()
        player = 1

        while True:
            if player == 1:
                move = model_move(model, game)
            else:
                if opponent == "random":
                    move = game.available_moves()[0]
                else:
                    move = teacher_move(game, -1)

            game.make_move(move, player)
            winner = game.check_winner()

            if winner is not None:
                if winner == 1: wins += 1
                elif winner == -1: losses += 1
                else: draws += 1
                break

            player *= -1

    print(f"\nEvaluation vs {opponent.upper()}")
    print("Wins:", wins)
    print("Losses:", losses)
    print("Draws:", draws)