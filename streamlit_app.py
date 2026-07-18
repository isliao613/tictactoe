import pathlib
import sys

import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, str(pathlib.Path(__file__).parent / "tictactoe"))
from game import ai_move, apply_move, check_winner

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
    /* square cells with a large centered mark */
    div[data-testid="stColumn"] div.stButton > button {
        aspect-ratio: 1 / 1;
        height: auto;
        font-size: 2.2rem;
        line-height: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎮 Tic Tac Toe")


def connection_badge():
    """Big, kid-friendly connection light: green when online, red when the
    network or the server drops, so it's obvious whether the game is still
    alive or has ended."""
    components.html(
        """
        <div id="conn" style="display:flex;align-items:center;gap:10px;
            font-family:'Source Sans Pro',sans-serif;font-size:20px;
            font-weight:700;padding:8px 14px;border-radius:12px;">
          <span id="dot" style="width:16px;height:16px;border-radius:50%;
            display:inline-block;"></span>
          <span id="txt"></span>
        </div>
        <script>
        const box = document.getElementById("conn");
        const dot = document.getElementById("dot");
        const txt = document.getElementById("txt");
        function ok() {
          dot.style.background = "#22c55e";
          dot.style.boxShadow = "0 0 10px #22c55e";
          txt.textContent = "🟢 已連線，可以開始玩！";
          txt.style.color = "#22c55e";
          box.style.background = "rgba(34,197,94,0.12)";
        }
        function bad() {
          dot.style.background = "#ef4444";
          dot.style.boxShadow = "0 0 10px #ef4444";
          txt.textContent = "🔴 連線中斷，請重新整理頁面";
          txt.style.color = "#ef4444";
          box.style.background = "rgba(239,68,68,0.15)";
        }
        function check() {
          if (navigator.onLine) { ok(); } else { bad(); }
        }
        window.addEventListener("online", ok);
        window.addEventListener("offline", bad);
        check();
        setInterval(check, 3000);
        </script>
        """,
        height=48,
    )


connection_badge()

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
if winner == "draw":
    st.info("🤝 平手！")
elif winner:
    st.success(f"🏆 {MARKS[winner]} {winner} 獲勝！")
else:
    turn = st.session_state.current
    st.caption(f"輪到 {MARKS[turn]} {turn}" + ("（你）" if mode == "ai" else ""))

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
