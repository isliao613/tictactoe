import random

import streamlit as st

from game_ui import back_home, square_cells

N = 4


def spawn(board):
    empties = [(r, c) for r in range(N) for c in range(N) if board[r][c] == 0]
    if empties:
        r, c = random.choice(empties)
        board[r][c] = 4 if random.random() < 0.1 else 2


def new_game():
    board = [[0] * N for _ in range(N)]
    spawn(board)
    spawn(board)
    st.session_state.g2_board = board
    st.session_state.g2_score = 0
    st.session_state.g2_over = False


if "g2_board" not in st.session_state:
    new_game()


def _merge_left(row):
    tiles = [v for v in row if v]
    out, gained, i = [], 0, 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            out.append(tiles[i] * 2)
            gained += tiles[i] * 2
            i += 2
        else:
            out.append(tiles[i])
            i += 1
    out += [0] * (N - len(out))
    return out, gained


def move(board, direction):
    b = [row[:] for row in board]
    if direction in ("up", "down"):
        b = [list(col) for col in zip(*b)]
    total = 0
    for i in range(N):
        row = b[i]
        rev = direction in ("right", "down")
        if rev:
            row = row[::-1]
        row, g = _merge_left(row)
        if rev:
            row = row[::-1]
        b[i] = row
        total += g
    if direction in ("up", "down"):
        b = [list(col) for col in zip(*b)]
    return b, total


def can_move(board):
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0:
                return True
            if c + 1 < N and board[r][c] == board[r][c + 1]:
                return True
            if r + 1 < N and board[r][c] == board[r + 1][c]:
                return True
    return False


def do(direction):
    board = st.session_state.g2_board
    new, gained = move(board, direction)
    if new != board:
        spawn(new)
        st.session_state.g2_board = new
        st.session_state.g2_score += gained
        if not can_move(new):
            st.session_state.g2_over = True


back_home()
st.title("🔢 2048")
square_cells("g2-cell", max_vh=15)

board = st.session_state.g2_board
st.caption(f"分數：{st.session_state.g2_score}　最大：{max(max(r) for r in board)}")

if st.session_state.g2_over:
    st.error("😵 沒有步可以走了！")
    st.button("🔄 再玩一次！", key="g2-restart", type="primary",
              use_container_width=True, on_click=new_game)
else:
    top = st.columns(3)
    top[1].button("⬆️", key="g2-up", use_container_width=True, on_click=do, args=("up",))
    mid = st.columns(3)
    mid[0].button("⬅️", key="g2-left", use_container_width=True, on_click=do, args=("left",))
    mid[1].button("⬇️", key="g2-down", use_container_width=True, on_click=do, args=("down",))
    mid[2].button("➡️", key="g2-right", use_container_width=True, on_click=do, args=("right",))

st.markdown(
    "<style>[class*='st-key-g2-cell'] button{font-size:clamp(1rem,5vh,1.8rem)!important;"
    "font-weight:700;}</style>",
    unsafe_allow_html=True,
)
for r in range(N):
    cols = st.columns(N, gap="small")
    for c in range(N):
        v = board[r][c]
        cols[c].button(str(v) if v else " ", key=f"g2-cell-{r}-{c}",
                       use_container_width=True, disabled=True)
