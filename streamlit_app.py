import pathlib
import sys

import streamlit as st

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tictactoe"))

from game_ui import GAMES, HOME

st.set_page_config(page_title="遊戲樂園", page_icon="🎮", layout="centered")

# Shared, kid-friendly styling for every page.
st.markdown(
    """
    <style>
    div[data-testid="stMainBlockContainer"] { padding-top: 2.2rem; }
    /* keep any column row (game boards) on a single line with equal cells */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0.4rem !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        min-width: 0 !important;
        flex: 1 1 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

pages = [st.Page(HOME, title="首頁", icon="🏠", default=True)]
pages += [st.Page(path, title=title, icon=icon) for path, title, icon, _ in GAMES]

st.navigation(pages).run()
