import random

import streamlit as st

from game_ui import back_home, square_cells

ROWS, COLS = 6, 7
TOKENS = {"R": "🔴", "Y": "🟡", None: "⚪"}


def init():
    st.session_state.c4 = [[None] * COLS for _ in range(ROWS)]
    st.session_state.c4_turn = "R"
    st.session_state.c4_winner = None


if "c4" not in st.session_state:
    init()


def drop_row(grid, col):
    for r in range(ROWS - 1, -1, -1):
        if grid[r][col] is None:
            return r
    return None


def check_win(grid, p):
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] != p:
                continue
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                if all(
                    0 <= r + dr * k < ROWS and 0 <= c + dc * k < COLS and grid[r + dr * k][c + dc * k] == p
                    for k in range(4)
                ):
                    return True
    return False


def valid_cols(grid):
    return [c for c in range(COLS) if grid[0][c] is None]


def ai_pick(grid, me, opp):
    for p in (me, opp):  # win first, then block
        for c in valid_cols(grid):
            r = drop_row(grid, c)
            grid[r][c] = p
            won = check_win(grid, p)
            grid[r][c] = None
            if won:
                return c
    cols = valid_cols(grid)
    return random.choice(sorted(cols, key=lambda c: abs(c - 3))[: min(3, len(cols))])


back_home()
st.title("🔴 四子棋")
square_cells("c4-cell", max_vh=11)

mode = st.radio("模式", ["ai", "pvp"], horizontal=True,
                format_func=lambda m: "🤖 對電腦" if m == "ai" else "👬 雙人")


def play(col):
    grid = st.session_state.c4
    r = drop_row(grid, col)
    if r is None:
        return
    p = st.session_state.c4_turn
    grid[r][col] = p
    if check_win(grid, p):
        st.session_state.c4_winner = p
        return
    if not valid_cols(grid):
        st.session_state.c4_winner = "draw"
        return
    nxt = "Y" if p == "R" else "R"
    if mode == "ai" and nxt == "Y":
        ac = ai_pick(grid, "Y", "R")
        ar = drop_row(grid, ac)
        grid[ar][ac] = "Y"
        if check_win(grid, "Y"):
            st.session_state.c4_winner = "Y"
        elif not valid_cols(grid):
            st.session_state.c4_winner = "draw"
    else:
        st.session_state.c4_turn = nxt


grid = st.session_state.c4
winner = st.session_state.c4_winner

if winner == "draw":
    st.info("🤝 平手！")
elif winner:
    st.success(f"🏆 {TOKENS[winner]} 連成四子，獲勝！")
else:
    st.caption(f"輪到 {TOKENS[st.session_state.c4_turn]}" +
               ("（你）" if mode == "ai" else ""))

if winner:
    st.button("🔄 再玩一次！", key="c4-restart", type="primary",
              use_container_width=True, on_click=init)

drop_cols = st.columns(COLS, gap="small")
for c in range(COLS):
    drop_cols[c].button("⬇️", key=f"c4-drop-{c}", use_container_width=True,
                        disabled=grid[0][c] is not None or winner is not None,
                        on_click=play, args=(c,))

for r in range(ROWS):
    cols = st.columns(COLS, gap="small")
    for c in range(COLS):
        cols[c].button(TOKENS[grid[r][c]], key=f"c4-cell-{r}-{c}",
                       use_container_width=True, disabled=True)
