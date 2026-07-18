import pathlib
import sys

import streamlit as st

sys.path.insert(0, str(pathlib.Path(__file__).parent / "tictactoe"))
from game import WIN_LINES, ai_move, apply_move, check_winner


def winning_line(board):
    """Return the three cells that form the winning row/col/diagonal, or ()."""
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return (a, b, c)
    return ()

st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮", layout="centered")

MARKS = {"X": "❌", "O": "⭕", None: ""}


def init_state():
    st.session_state.board = [None] * 9
    st.session_state.current = "X"
    st.session_state.winner = None


if "board" not in st.session_state:
    init_state()

st.markdown(
    """
    <style>
    /* trim the default top padding so the board has more vertical room */
    div[data-testid="stMainBlockContainer"] {
        padding-top: 2.5rem;
    }
    /* keep the 3-column board as a real grid even on narrow screens */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0.5rem !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        min-width: 0 !important;
        width: calc((100% - 1rem) / 3) !important;
        flex: 1 1 0 !important;
    }
    /* square cells with a large centered mark; cap size by viewport height
       so the 3x3 board never overflows (e.g. tablet in landscape) */
    div[data-testid="stColumn"] div.stButton > button {
        aspect-ratio: 1 / 1;
        height: auto;
        width: 100%;
        max-width: 18vh;
        display: block;
        margin-left: auto;
        margin-right: auto;
        font-size: clamp(1.4rem, 9vh, 2.6rem);
        line-height: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎮 Tic Tac Toe")

with st.sidebar:
    st.header("設定")
    mode = st.radio("模式", ["ai", "pvp"], format_func=lambda m: "單人 (vs AI)" if m == "ai" else "雙人對戰")
    difficulty = "easy"
    if mode == "ai":
        difficulty = st.radio("難度", ["easy", "hard"], index=1, format_func=lambda d: "簡單" if d == "easy" else "困難")
    if st.button("🔄 重新開始", use_container_width=True):
        init_state()
        st.rerun()


def play(cell: int):
    board = st.session_state.board
    player = st.session_state.current
    board = apply_move(board, cell, player)
    winner = check_winner(board)

    if winner is None and mode == "ai":
        ai_player = "O" if player == "X" else "X"
        board = apply_move(board, ai_move(board, ai_player, difficulty), ai_player)
        winner = check_winner(board)
    elif winner is None:
        st.session_state.current = "O" if player == "X" else "X"

    st.session_state.board = board
    st.session_state.winner = winner


winner = st.session_state.winner
win_cells = winning_line(st.session_state.board)

if win_cells:
    highlight = "".join(
        f".st-key-cell-{i} div.stButton > button {{"
        "background:#22c55e !important;border-color:#16a34a !important;"
        "color:#fff !important;box-shadow:0 0 16px #22c55e;}"
        for i in win_cells
    )
    st.markdown(f"<style>{highlight}</style>", unsafe_allow_html=True)

if winner == "draw":
    st.info("🤝 平手！")
elif winner:
    st.success(f"🏆 {MARKS[winner]} {winner} 連成一線，獲勝！")
else:
    turn = st.session_state.current
    st.caption(f"輪到 {MARKS[turn]} {turn}" + ("（你）" if mode == "ai" else ""))

if winner:
    st.button(
        "🔄 再玩一次！",
        key="restart-main",
        type="primary",
        use_container_width=True,
        on_click=init_state,
    )

for row in range(3):
    cols = st.columns(3, gap="small")
    for col in range(3):
        cell = row * 3 + col
        mark = st.session_state.board[cell]
        cols[col].button(
            MARKS[mark] or " ",
            key=f"cell-{cell}",
            use_container_width=True,
            disabled=mark is not None or winner is not None,
            on_click=play,
            args=(cell,),
        )
