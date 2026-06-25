import pytest
from game import check_winner, apply_move

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
