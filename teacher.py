import random

def teacher_move(game, player):
    opponent = -player

    # Win if possible
    for move in game.available_moves():
        game.board[move] = player
        if game.check_winner() == player:
            game.board[move] = 0
            return move
        game.board[move] = 0

    # Block opponent
    for move in game.available_moves():
        game.board[move] = opponent
        if game.check_winner() == opponent:
            game.board[move] = 0
            return move
        game.board[move] = 0

    # Center
    if 4 in game.available_moves():
        return 4

    # Corners
    corners = [0,2,6,8]
    random.shuffle(corners)
    for c in corners:
        if c in game.available_moves():
            return c

    return random.choice(game.available_moves())