import pygame
from game import TicTacToe
from evaluate import model_move

BOARD_SIZE = 540
TOP_PANEL = 110
BOTTOM_PANEL = 70
WINDOW_WIDTH = BOARD_SIZE
WINDOW_HEIGHT = TOP_PANEL + BOARD_SIZE + BOTTOM_PANEL
CELL = BOARD_SIZE // 3
BOARD_TOP = TOP_PANEL

BG_COLOR = (245, 248, 252)
PANEL_COLOR = (231, 237, 246)
GRID_COLOR = (66, 84, 112)
X_COLOR = (220, 62, 62)
O_COLOR = (48, 108, 212)
HOVER_COLOR = (194, 214, 250)
TEXT_DARK = (31, 40, 55)
TEXT_MUTED = (97, 109, 130)
WIN_LINE_COLOR = (28, 163, 102)

WIN_LINES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6],
]


def get_winning_line(board):
    for line in WIN_LINES:
        total = sum(board[line])
        if total == 3 or total == -3:
            return line
    return None


def get_cell_rect(cell_index):
    row, col = divmod(cell_index, 3)
    return pygame.Rect(col * CELL, BOARD_TOP + row * CELL, CELL, CELL)


def draw_x(screen, rect):
    margin = int(CELL * 0.23)
    start1 = (rect.left + margin, rect.top + margin)
    end1 = (rect.right - margin, rect.bottom - margin)
    start2 = (rect.left + margin, rect.bottom - margin)
    end2 = (rect.right - margin, rect.top + margin)
    pygame.draw.line(screen, X_COLOR, start1, end1, 10)
    pygame.draw.line(screen, X_COLOR, start2, end2, 10)


def draw_o(screen, rect):
    center = rect.center
    radius = int(CELL * 0.28)
    pygame.draw.circle(screen, O_COLOR, center, radius, 10)


def draw_board(screen, game, status_text, sub_text, hover_cell=None, winning_line=None):
    screen.fill(BG_COLOR)

    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WINDOW_WIDTH, TOP_PANEL))
    pygame.draw.rect(screen, PANEL_COLOR, (0, TOP_PANEL + BOARD_SIZE, WINDOW_WIDTH, BOTTOM_PANEL))

    title_font = pygame.font.SysFont("Segoe UI", 40, bold=True)
    status_font = pygame.font.SysFont("Segoe UI", 28, bold=True)
    info_font = pygame.font.SysFont("Segoe UI", 22)

    title = title_font.render("Tic Tac Toe", True, TEXT_DARK)
    status = status_font.render(status_text, True, TEXT_DARK)
    info = info_font.render(sub_text, True, TEXT_MUTED)

    screen.blit(title, (18, 14))
    screen.blit(status, (18, 58))
    screen.blit(info, (18, TOP_PANEL + BOARD_SIZE + 22))

    if hover_cell is not None and game.board[hover_cell] == 0 and winning_line is None:
        hover_rect = get_cell_rect(hover_cell)
        inner = hover_rect.inflate(-14, -14)
        pygame.draw.rect(screen, HOVER_COLOR, inner, border_radius=12)

    for i in range(1, 3):
        y = BOARD_TOP + i * CELL
        x = i * CELL
        pygame.draw.line(screen, GRID_COLOR, (0, y), (BOARD_SIZE, y), 6)
        pygame.draw.line(screen, GRID_COLOR, (x, BOARD_TOP), (x, BOARD_TOP + BOARD_SIZE), 6)

    for i in range(9):
        rect = get_cell_rect(i)
        if game.board[i] == 1:
            draw_x(screen, rect)
        elif game.board[i] == -1:
            draw_o(screen, rect)

    if winning_line is not None:
        start_rect = get_cell_rect(winning_line[0])
        end_rect = get_cell_rect(winning_line[2])
        pygame.draw.line(screen, WIN_LINE_COLOR, start_rect.center, end_rect.center, 12)


def run_gui(model):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("ANN Tic Tac Toe")
    clock = pygame.time.Clock()

    game = TicTacToe()
    player = 1
    running = True
    game_over_at = None
    winner = None

    while running:
        hover_cell = None
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 0 <= mouse_x < BOARD_SIZE and BOARD_TOP <= mouse_y < BOARD_TOP + BOARD_SIZE:
            hover_cell = ((mouse_y - BOARD_TOP) // CELL) * 3 + (mouse_x // CELL)

        if winner is None:
            winner = game.check_winner()
            if winner is not None:
                game_over_at = pygame.time.get_ticks()

        winning_line = get_winning_line(game.board) if winner in (1, -1) else None

        if winner is None:
            status_text = "Your turn (X)" if player == 1 else "Model is thinking..."
            sub_text = "Click an empty cell to place X. Press R to restart, Esc to quit."
        elif winner == 1:
            status_text = "You win!"
            sub_text = "New game starts automatically in 2 seconds. Press R for instant restart."
        elif winner == -1:
            status_text = "Model wins."
            sub_text = "New game starts automatically in 2 seconds. Press R for instant restart."
        else:
            status_text = "It's a draw."
            sub_text = "New game starts automatically in 2 seconds. Press R for instant restart."

        draw_board(screen, game, status_text, sub_text, hover_cell, winning_line)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game.reset()
                    player = 1
                    winner = None
                    game_over_at = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and player == 1 and winner is None:
                x, y = pygame.mouse.get_pos()
                if 0 <= x < BOARD_SIZE and BOARD_TOP <= y < BOARD_TOP + BOARD_SIZE:
                    move = ((y - BOARD_TOP) // CELL) * 3 + (x // CELL)
                    if game.make_move(move, 1):
                        player = -1

        # Model move
        if player == -1 and winner is None:
            if len(game.available_moves()) > 0:
                pygame.time.delay(300)
                move = model_move(model, game)
                game.make_move(move, -1)
                player = 1

        if winner is not None and game_over_at is not None:
            elapsed = pygame.time.get_ticks() - game_over_at
            if elapsed >= 2000:
                game.reset()
                player = 1
                winner = None
                game_over_at = None

        clock.tick(60)

    pygame.quit()
