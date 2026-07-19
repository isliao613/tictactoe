import streamlit as st

HOME = "game_pages/home.py"

GAMES = [
    ("game_pages/tic_tac_toe.py", "井字遊戲", "⭕", "三個連成一線就贏，可跟電腦對戰"),
    ("game_pages/connect_four.py", "四子棋", "🔴", "把棋子丟下去，四顆連線獲勝"),
    ("game_pages/memory.py", "記憶翻牌", "🃏", "翻開兩張一樣的圖案來配對"),
    ("game_pages/guess_number.py", "猜數字", "🔢", "用最少次數猜中神秘數字"),
    ("game_pages/whack.py", "打地鼠", "🔨", "地鼠冒出來就打，看能連幾隻"),
    ("game_pages/quiz.py", "配對測驗", "🎨", "認顏色、水果和動物"),
    ("game_pages/game_2048.py", "2048", "🔢", "合併數字，挑戰 2048"),
    ("game_pages/sudoku.py", "數獨 4×4", "🧩", "把 1~4 填滿每行每列"),
]


def square_cells(key_substring, max_vh=18):
    """Make board buttons whose Streamlit key contains ``key_substring`` render
    as large square cells, capped by viewport height so the board never
    overflows on short landscape screens."""
    st.markdown(
        f"""
        <style>
        [class*="st-key-{key_substring}"] div.stButton > button {{
            aspect-ratio: 1 / 1;
            height: auto;
            width: 100%;
            max-width: {max_vh}vh;
            display: block;
            margin-left: auto;
            margin-right: auto;
            font-size: clamp(1.1rem, {max_vh // 2}vh, 2.4rem);
            line-height: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def back_home():
    st.page_link(HOME, label="🏠 回首頁")
