import random

WIN_LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6),
]

def check_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(cell is not None for cell in board):
        return "draw"
    return None

def apply_move(board, cell, player):
    if cell < 0 or cell > 8:
        raise ValueError(f"Cell {cell} out of range")
    if board[cell] is not None:
        raise ValueError(f"Cell {cell} is already occupied")
    new_board = board.copy()
    new_board[cell] = player
    return new_board

def ai_move(board, ai_player, difficulty):
    empty = [i for i, cell in enumerate(board) if cell is None]
    if difficulty == "easy":
        return random.choice(empty)
    return _best_move(board, ai_player)

def _best_move(board, ai_player):
    opponent = "O" if ai_player == "X" else "X"
    best_score = -2
    best_cell = None
    for cell in [i for i, c in enumerate(board) if c is None]:
        board[cell] = ai_player
        score = _minimax(board, False, ai_player, opponent, -2, 2)
        board[cell] = None
        if score > best_score:
            best_score = score
            best_cell = cell
    return best_cell

def _minimax(board, is_maximizing, ai_player, opponent, alpha, beta):
    winner = check_winner(board)
    if winner == ai_player:
        return 1
    if winner == opponent:
        return -1
    if winner == "draw":
        return 0

    if is_maximizing:
        best = -2
        for i in [c for c, v in enumerate(board) if v is None]:
            board[i] = ai_player
            best = max(best, _minimax(board, False, ai_player, opponent, alpha, beta))
            board[i] = None
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = 2
        for i in [c for c, v in enumerate(board) if v is None]:
            board[i] = opponent
            best = min(best, _minimax(board, True, ai_player, opponent, alpha, beta))
            board[i] = None
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best
