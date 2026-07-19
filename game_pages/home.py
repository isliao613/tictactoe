import streamlit as st

from game_ui import GAMES

st.title("🎮 遊戲樂園")
st.caption("挑一個遊戲開始玩吧！")

for i in range(0, len(GAMES), 2):
    cols = st.columns(2, gap="medium")
    for col, (path, title, icon, desc) in zip(cols, GAMES[i : i + 2]):
        with col:
            st.page_link(path, label=f"{icon}  {title}", use_container_width=True)
            st.caption(desc)
