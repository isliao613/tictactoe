import random

import streamlit as st

from game_ui import back_home, square_cells

PUZZLES = [
    [[1, 0, 0, 4], [0, 4, 1, 0], [0, 1, 4, 0], [4, 0, 0, 1]],
    [[2, 0, 1, 0], [0, 3, 0, 4], [4, 0, 3, 0], [0, 1, 0, 2]],
    [[0, 4, 0, 3], [3, 0, 2, 0], [0, 2, 0, 1], [1, 0, 4, 0]],
]


def new_game():
    puz = random.choice(PUZZLES)
    st.session_state.sk_grid = [row[:] for row in puz]
    st.session_state.sk_given = [[v != 0 for v in row] for row in puz]
    st.session_state.sk_sel = None


if "sk_grid" not in st.session_state:
    new_game()


def valid_solution(g):
    groups = []
    groups += [g[r] for r in range(4)]
    groups += [[g[r][c] for r in range(4)] for c in range(4)]
    for br in (0, 2):
        for bc in (0, 2):
            groups.append([g[br + i][bc + j] for i in range(2) for j in range(2)])
    return all(sorted(grp) == [1, 2, 3, 4] for grp in groups)


def select(r, c):
    if not st.session_state.sk_given[r][c]:
        st.session_state.sk_sel = (r, c)


def put(n):
    sel = st.session_state.sk_sel
    if sel:
        st.session_state.sk_grid[sel[0]][sel[1]] = n


back_home()
st.title("🧩 數獨 4×4")
st.caption("每一行、每一列、每個 2×2 方格都要有 1~4，不能重複。先點空格，再點下面的數字。")
square_cells("sk-cell", max_vh=16)

grid = st.session_state.sk_grid
sel = st.session_state.sk_sel
solved = all(all(v != 0 for v in row) for row in grid) and valid_solution(grid)

if solved:
    st.success("🎉 完成了！全部正確！")
    st.button("🔄 換一題", key="sk-restart", type="primary",
              use_container_width=True, on_click=new_game)

# highlight selected + dim givens
css = "[class*='st-key-sk-cell'] button{font-size:1.8rem!important;font-weight:700;}"
if sel:
    css += (f"[class*='st-key-sk-cell-{sel[0]}-{sel[1]}'] button"
            "{background:#7c6cf0 !important;color:#fff !important;}")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

for r in range(4):
    cols = st.columns(4, gap="small")
    for c in range(4):
        v = grid[r][c]
        given = st.session_state.sk_given[r][c]
        cols[c].button(str(v) if v else " ", key=f"sk-cell-{r}-{c}",
                       use_container_width=True, disabled=given or solved,
                       on_click=select, args=(r, c))

st.write("")
pad = st.columns(5, gap="small")
for i, n in enumerate([1, 2, 3, 4]):
    pad[i].button(str(n), key=f"sk-num-{n}", use_container_width=True,
                  disabled=sel is None or solved, on_click=put, args=(n,))
pad[4].button("🧹", key="sk-num-0", use_container_width=True,
              disabled=sel is None or solved, on_click=put, args=(0,))
