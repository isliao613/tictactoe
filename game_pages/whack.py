import random

import streamlit as st

from game_ui import back_home, square_cells

HOLE, MOLE, BOOM = "🕳️", "🐹", "💥"


def new_game():
    st.session_state.wk_mole = random.randint(0, 8)
    st.session_state.wk_score = 0
    st.session_state.wk_over = False
    st.session_state.wk_boom = None


if "wk_mole" not in st.session_state:
    new_game()
    st.session_state.wk_best = 0

back_home()
st.title("🔨 打地鼠")
square_cells("wk-cell", max_vh=18)


def hit(i):
    if st.session_state.wk_over:
        return
    if i == st.session_state.wk_mole:
        st.session_state.wk_score += 1
        choices = [x for x in range(9) if x != i]
        st.session_state.wk_mole = random.choice(choices)
    else:
        st.session_state.wk_over = True
        st.session_state.wk_boom = i
        st.session_state.wk_best = max(st.session_state.wk_best, st.session_state.wk_score)


score, best = st.session_state.wk_score, st.session_state.wk_best
if st.session_state.wk_over:
    st.error(f"💥 打錯了！這次打了 {score} 隻　🏅 最佳：{best}")
    st.button("🔄 再玩一次！", key="wk-restart", type="primary",
              use_container_width=True, on_click=new_game)
else:
    st.success(f"🐹 打到地鼠加分！　分數：{score}　🏅 最佳：{best}")
    st.caption("點到沒有地鼠的洞就結束囉！")

for r in range(3):
    cols = st.columns(3, gap="small")
    for c in range(3):
        i = r * 3 + c
        if st.session_state.wk_over and i == st.session_state.wk_boom:
            label = BOOM
        elif i == st.session_state.wk_mole:
            label = MOLE
        else:
            label = HOLE
        cols[c].button(label, key=f"wk-cell-{i}", use_container_width=True,
                       disabled=st.session_state.wk_over, on_click=hit, args=(i,))
