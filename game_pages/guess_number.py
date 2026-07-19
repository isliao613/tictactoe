import random

import streamlit as st

from game_ui import back_home

MAX = 100


def new_game():
    st.session_state.gn_target = random.randint(1, MAX)
    st.session_state.gn_tries = 0
    st.session_state.gn_hint = f"我想了一個 1 到 {MAX} 的數字，猜猜看！"
    st.session_state.gn_done = False
    st.session_state.gn_lo, st.session_state.gn_hi = 1, MAX


if "gn_target" not in st.session_state:
    new_game()

back_home()
st.title("🔢 猜數字")
st.caption(f"目前範圍：{st.session_state.gn_lo} ~ {st.session_state.gn_hi}")

guess = st.number_input("你猜幾？", min_value=1, max_value=MAX, step=1,
                        value=(st.session_state.gn_lo + st.session_state.gn_hi) // 2,
                        disabled=st.session_state.gn_done)


def check():
    g = int(guess)
    st.session_state.gn_tries += 1
    t = st.session_state.gn_target
    if g == t:
        st.session_state.gn_hint = f"🎉 猜中了！答案是 {t}，你猜了 {st.session_state.gn_tries} 次"
        st.session_state.gn_done = True
    elif g < t:
        st.session_state.gn_lo = max(st.session_state.gn_lo, g + 1)
        st.session_state.gn_hint = f"⬆️ 太小了！再大一點（第 {st.session_state.gn_tries} 次）"
    else:
        st.session_state.gn_hi = min(st.session_state.gn_hi, g - 1)
        st.session_state.gn_hint = f"⬇️ 太大了！再小一點（第 {st.session_state.gn_tries} 次）"


if not st.session_state.gn_done:
    st.button("🎯 猜！", key="gn-guess", type="primary",
              use_container_width=True, on_click=check)

if st.session_state.gn_done:
    st.success(st.session_state.gn_hint)
    st.button("🔄 再玩一次！", key="gn-restart", type="primary",
              use_container_width=True, on_click=new_game)
else:
    st.info(st.session_state.gn_hint)
