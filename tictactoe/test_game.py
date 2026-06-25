import pytest
from game import check_winner, apply_move, ai_move

def test_x_wins_top_row():
    board = ["X","X","X", None,None,None, None,None,None]
    assert check_winner(board) == "X"

def test_o_wins_left_col():
    board = ["O",None,None, "O",None,None, "O",None,None]
    assert check_winner(board) == "O"

def test_x_wins_diagonal():
    board = ["X",None,None, None,"X",None, None,None,"X"]
    assert check_winner(board) == "X"

def test_draw():
    board = ["X","O","X", "X","X","O", "O","X","O"]
    assert check_winner(board) == "draw"

def test_no_winner_yet():
    board = ["X","O",None, None,None,None, None,None,None]
    assert check_winner(board) is None

def test_apply_move_empty_cell():
    board = [None]*9
    new_board = apply_move(board, 4, "X")
    assert new_board[4] == "X"
    assert new_board is not board

def test_apply_move_occupied_raises():
    board = ["X"] + [None]*8
    with pytest.raises(ValueError):
        apply_move(board, 0, "O")

def test_apply_move_out_of_range_raises():
    board = [None]*9
    with pytest.raises(ValueError):
        apply_move(board, 9, "X")

def test_ai_easy_returns_valid_cell():
    board = ["X","O","X", None,"O",None, None,None,None]
    cell = ai_move(board, "O", "easy")
    assert cell in [3, 5, 6, 7, 8]

def test_ai_hard_takes_win():
    # O can win by playing cell 2
    board = ["O","O",None, "X","X",None, None,None,None]
    assert ai_move(board, "O", "hard") == 2

def test_ai_hard_blocks_human_win():
    # X would win at cell 2 — AI must block
    board = ["X","X",None, "O",None,None, None,None,None]
    assert ai_move(board, "O", "hard") == 2

def test_ai_hard_never_loses():
    """Minimax vs minimax from an empty board must always draw."""
    def play_out(board, current):
        winner = check_winner(board)
        if winner:
            return winner
        cell = ai_move(board, current, "hard")
        new_board = apply_move(board, cell, current)
        next_player = "O" if current == "X" else "X"
        return play_out(new_board, next_player)

    result = play_out([None]*9, "X")
    assert result == "draw"
