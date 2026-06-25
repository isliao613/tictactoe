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
