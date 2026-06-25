from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
EMPTY = [None] * 9

def test_reset_returns_empty_board():
    resp = client.post("/reset")
    assert resp.status_code == 200
    data = resp.json()
    assert data["board"] == EMPTY
    assert data["winner"] is None
    assert data["next_player"] == "X"

def test_move_updates_board():
    resp = client.post("/move", json={
        "board": EMPTY, "cell": 4, "player": "X", "mode": "2p", "difficulty": "easy"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["board"][4] == "X"
    assert data["winner"] is None
    assert data["next_player"] == "O"

def test_move_detects_winner():
    board = ["X","X",None, "O","O",None, None,None,None]
    resp = client.post("/move", json={
        "board": board, "cell": 2, "player": "X", "mode": "2p", "difficulty": "easy"
    })
    assert resp.status_code == 200
    assert resp.json()["winner"] == "X"

def test_move_occupied_cell_returns_400():
    board = ["X"] + [None]*8
    resp = client.post("/move", json={
        "board": board, "cell": 0, "player": "O", "mode": "2p", "difficulty": "easy"
    })
    assert resp.status_code == 400

def test_ai_mode_applies_ai_move():
    resp = client.post("/move", json={
        "board": EMPTY, "cell": 4, "player": "X", "mode": "ai", "difficulty": "easy"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["board"][4] == "X"
    o_cells = [i for i, v in enumerate(data["board"]) if v == "O"]
    assert len(o_cells) == 1
