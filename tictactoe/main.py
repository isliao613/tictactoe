from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import pathlib
from game import check_winner, apply_move, ai_move

app = FastAPI()

STATIC = pathlib.Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC), name="static")

@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")

class MoveRequest(BaseModel):
    board: list[Optional[str]]
    cell: int
    player: str
    mode: str
    difficulty: str

class GameState(BaseModel):
    board: list[Optional[str]]
    winner: Optional[str]
    next_player: str

@app.post("/move", response_model=GameState)
def move(req: MoveRequest):
    try:
        board = apply_move(req.board, req.cell, req.player)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    winner = check_winner(board)
    if winner:
        return GameState(board=board, winner=winner, next_player=req.player)

    if req.mode == "ai":
        ai_player = "O" if req.player == "X" else "X"
        cell = ai_move(board, ai_player, req.difficulty)
        board = apply_move(board, cell, ai_player)
        winner = check_winner(board)
        next_player = req.player
    else:
        next_player = "O" if req.player == "X" else "X"

    return GameState(board=board, winner=winner, next_player=next_player)

@app.post("/reset", response_model=GameState)
def reset():
    return GameState(board=[None]*9, winner=None, next_player="X")
