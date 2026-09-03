import streamlit as st

from game.state import initialize_state, select_level
from game.ui import apply_global_styles, show_startup_splash


st.set_option("client.toolbarMode", "minimal")
st.set_option("client.showErrorDetails", "none")

st.set_page_config(
    page_title="Physics Around Us",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()
initialize_state()
requested_level = st.query_params.get("level")
if requested_level in {"kitchen_01", "study_room_01", "water_garden_01"}:
    select_level(requested_level)
show_startup_splash()

open_level = st.query_params.get("view") == "level"
pages = [
    st.Page("pages/home.py", title="Home", icon="🏠", default=not open_level),
    st.Page("pages/level.py", title="Level", icon="🔬", default=open_level),
    st.Page("pages/results.py", title="Results", icon="🏆"),
]

navigation = st.navigation(pages, position="hidden")
navigation.run()
