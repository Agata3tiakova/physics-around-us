from base64 import b64encode
from pathlib import Path

import streamlit as st


STYLE_PATH = Path(__file__).resolve().parent.parent / "assets" / "app.css"
UI_ASSET_DIR = STYLE_PATH.parent / "ui"


@st.cache_data(show_spinner=False)
def asset_data_uri(path_value: str, modified_ns: int) -> str:
    del modified_ns
    path = Path(path_value)
    media_type = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    encoded = b64encode(path.read_bytes()).decode("ascii")
    return f"data:{media_type};base64,{encoded}"


def apply_global_styles() -> None:
    styles = STYLE_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)


def ui_asset_data_uri(filename: str) -> str:
    path = UI_ASSET_DIR / filename
    return asset_data_uri(str(path), path.stat().st_mtime_ns)


def render_level_navigation() -> None:
    from game.level_loader import load_levels
    from game.state import select_level

    current_level_id = st.session_state.current_level
    saved_states = st.session_state.get("level_states", {})

    st.markdown('<div class="level-nav-marker">Levels</div>', unsafe_allow_html=True)
    for level in load_levels():
        level_id = level["id"]
        if level_id == current_level_id:
            found_count = len(st.session_state.found_objects)
        else:
            found_count = len(saved_states.get(level_id, {}).get("found_objects", []))

        total_count = len(level["objects"])
        is_current = level_id == current_level_id
        if st.button(
            f"{level['number']}. {level.get('nav_title', level['title'])} - {found_count}/{total_count}",
            key=f"sidebar-level-{level_id}",
            type="primary" if is_current else "secondary",
            icon=":material/radio_button_checked:" if is_current else ":material/radio_button_unchecked:",
            use_container_width=True,
        ):
            st.query_params["level"] = level_id
            st.query_params["view"] = "level"
            select_level(level_id)
            st.switch_page("pages/level.py")


def show_startup_splash() -> None:
    if st.session_state.get("startup_splash_seen"):
        return

    background = ui_asset_data_uri("loading-stripes.jpg")
    mark = ui_asset_data_uri("topic-electricity.png")
    st.markdown(
        f"""
        <div class="startup-splash" style="--splash-bg: url('{background}')">
            <div class="startup-splash__mark">
                <img src="{mark}" alt="" />
                <span>Opening the lab</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.startup_splash_seen = True
