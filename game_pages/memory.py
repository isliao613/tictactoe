import random

import streamlit as st

from game_ui import back_home, square_cells

POOL = ["🐶", "🐱", "🐭", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐸", "🐵", "🦄", "🐷"]
BACK = "🎴"
COLS = 4


def new_game(pairs):
    cards = random.sample(POOL, pairs) * 2
    random.shuffle(cards)
    st.session_state.mem_cards = cards
    st.session_state.mem_matched = set()
    st.session_state.mem_flipped = []
    st.session_state.mem_moves = 0
    st.session_state.mem_pairs = pairs


back_home()
st.title("🃏 記憶翻牌")

pairs = st.radio("難度", [4, 8], horizontal=True, index=1,
                 format_func=lambda n: f"{'😀 簡單' if n == 4 else '🧠 普通'}（{n} 對）")

if "mem_cards" not in st.session_state or st.session_state.get("mem_pairs") != pairs:
    new_game(pairs)

square_cells("mem-card", max_vh=16)


def flip(i):
    matched, flipped = st.session_state.mem_matched, st.session_state.mem_flipped
    if i in matched or i in flipped:
        return
    if len(flipped) == 2:
        flipped = []
    flipped.append(i)
    if len(flipped) == 2:
        st.session_state.mem_moves += 1
        a, b = flipped
        if st.session_state.mem_cards[a] == st.session_state.mem_cards[b]:
            matched.update((a, b))
            flipped = []
    st.session_state.mem_flipped = flipped


cards = st.session_state.mem_cards
matched = st.session_state.mem_matched
flipped = st.session_state.mem_flipped
done = len(matched) == len(cards)

if done:
    st.success(f"🎉 全部配對成功！用了 {st.session_state.mem_moves} 步")
    st.button("🔄 再玩一次！", key="mem-restart", type="primary",
              use_container_width=True, on_click=new_game, args=(pairs,))
else:
    st.caption(f"步數：{st.session_state.mem_moves}　已配對：{len(matched) // 2} / {len(cards) // 2}")

for r in range((len(cards) + COLS - 1) // COLS):
    cols = st.columns(COLS, gap="small")
    for c in range(COLS):
        i = r * COLS + c
        if i >= len(cards):
            continue
        face_up = i in matched or i in flipped
        cols[c].button(cards[i] if face_up else BACK, key=f"mem-card-{i}",
                       use_container_width=True,
                       disabled=face_up or done, on_click=flip, args=(i,))
