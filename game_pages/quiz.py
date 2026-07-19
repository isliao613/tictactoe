import random

import streamlit as st

from game_ui import back_home

ITEMS = [
    ("紅色", "🔴"), ("藍色", "🔵"), ("綠色", "🟢"), ("黃色", "🟡"),
    ("紫色", "🟣"), ("橘色", "🟠"),
    ("蘋果", "🍎"), ("香蕉", "🍌"), ("草莓", "🍓"), ("葡萄", "🍇"),
    ("西瓜", "🍉"), ("鳳梨", "🍍"),
    ("小狗", "🐶"), ("小貓", "🐱"), ("兔子", "🐰"), ("獅子", "🦁"),
    ("大象", "🐘"), ("企鵝", "🐧"),
]


def new_question():
    target = random.choice(ITEMS)
    others = random.sample([x for x in ITEMS if x != target], 3)
    opts = others + [target]
    random.shuffle(opts)
    st.session_state.qz_target = target
    st.session_state.qz_opts = opts


def new_game():
    st.session_state.qz_score = 0
    st.session_state.qz_total = 0
    st.session_state.qz_msg = "點出題目對應的圖案吧！"
    new_question()


if "qz_target" not in st.session_state:
    new_game()

back_home()
st.title("🎨 配對測驗")

name, emoji = st.session_state.qz_target
st.markdown(f"<h2 style='text-align:center'>找出：{name}</h2>", unsafe_allow_html=True)
st.caption(f"{st.session_state.qz_msg}　　答對 {st.session_state.qz_score} / {st.session_state.qz_total}")


def answer(choice_emoji):
    st.session_state.qz_total += 1
    if choice_emoji == emoji:
        st.session_state.qz_score += 1
        st.session_state.qz_msg = "✅ 答對了！下一題～"
        new_question()
    else:
        st.session_state.qz_msg = "❌ 不對喔，再試一次！"


cols = st.columns(4, gap="small")
for col, (_, e) in zip(cols, st.session_state.qz_opts):
    col.button(e, key=f"qz-opt-{e}", use_container_width=True,
               on_click=answer, args=(e,))

st.markdown(
    "<style>[class*='st-key-qz-opt'] button{font-size:2.4rem;height:5rem;}</style>",
    unsafe_allow_html=True,
)
st.button("🔄 重新計分", key="qz-restart", on_click=new_game)
