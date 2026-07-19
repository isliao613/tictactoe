import streamlit as st

from game import WIN_LINES, ai_move, apply_move, check_winner
from game_ui import back_home, square_cells

MARKS = {"X": "❌", "O": "⭕", None: " "}


def winning_line(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return (a, b, c)
    return ()


def init():
    st.session_state.ttt_board = [None] * 9
    st.session_state.ttt_current = "X"
    st.session_state.ttt_winner = None


if "ttt_board" not in st.session_state:
    init()

back_home()
st.title("⭕ 井字遊戲")
square_cells("ttt-cell", max_vh=18)

c1, c2 = st.columns(2)
mode = c1.radio("模式", ["ai", "pvp"], horizontal=True,
                format_func=lambda m: "🤖 對電腦" if m == "ai" else "👬 雙人")
difficulty = "hard"
if mode == "ai":
    difficulty = c2.radio("難度", ["easy", "hard"], index=1, horizontal=True,
                          format_func=lambda d: "😀 簡單" if d == "easy" else "😈 困難")


def play(cell):
    board = apply_move(st.session_state.ttt_board, cell, st.session_state.ttt_current)
    winner = check_winner(board)
    if winner is None and mode == "ai":
        ai_p = "O" if st.session_state.ttt_current == "X" else "X"
        board = apply_move(board, ai_move(board, ai_p, difficulty), ai_p)
        winner = check_winner(board)
    elif winner is None:
        st.session_state.ttt_current = "O" if st.session_state.ttt_current == "X" else "X"
    st.session_state.ttt_board = board
    st.session_state.ttt_winner = winner


board = st.session_state.ttt_board
winner = st.session_state.ttt_winner
win_cells = winning_line(board)

if win_cells:
    hl = "".join(
        f'[class*="st-key-ttt-cell-{i}"] div.stButton > button {{'
        "background:#22c55e !important;border-color:#16a34a !important;"
        "color:#fff !important;box-shadow:0 0 16px #22c55e;}"
        for i in win_cells
    )
    st.markdown(f"<style>{hl}</style>", unsafe_allow_html=True)

if winner == "draw":
    st.info("🤝 平手！")
elif winner:
    st.success(f"🏆 {MARKS[winner]} {winner} 連成一線，獲勝！")
else:
    turn = st.session_state.ttt_current
    st.caption(f"輪到 {MARKS[turn]} {turn}" + ("（你）" if mode == "ai" else ""))

if winner:
    st.button("🔄 再玩一次！", key="ttt-restart", type="primary",
              use_container_width=True, on_click=init)

for row in range(3):
    cols = st.columns(3, gap="small")
    for col in range(3):
        cell = row * 3 + col
        cols[col].button(
            MARKS[board[cell]],
            key=f"ttt-cell-{cell}",
            use_container_width=True,
            disabled=board[cell] is not None or winner is not None,
            on_click=play,
            args=(cell,),
        )
