from base64 import b64encode
from pathlib import Path

import streamlit as st
from streamlit.components.v2 import component


COMPONENT_DIR = Path(__file__).parent
KITCHEN_SPRITE_PATHS = {
    "box": COMPONENT_DIR / "box-v2.png",
    "cat_sitting": COMPONENT_DIR / "cat-sitting-v3.png",
    "cat_crouching": COMPONENT_DIR / "cat-crouching-v3.png",
    "cat_jumping": COMPONENT_DIR / "cat-jumping-v3.png",
    "kettle": COMPONENT_DIR / "kettle-v2.png",
    "soup_pot": COMPONENT_DIR / "soup-pot-v2.png",
}


@st.cache_data(show_spinner=False)
def _asset_data_url(path_value: str, modified_ns: int) -> str:
    del modified_ns
    path = Path(path_value)
    encoded = b64encode(path.read_bytes()).decode("ascii")
    mime_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(path.suffix.lower(), "image/png")
    return f"data:{mime_type};base64,{encoded}"


_scene_component = component(
    "physics_scene",
    html='<main id="scene" aria-label="Interactive physics scene"></main>',
    css=(COMPONENT_DIR / "scene.css").read_text(encoding="utf-8"),
    js=(COMPONENT_DIR / "scene.js").read_text(encoding="utf-8"),
)


def physics_scene(
    level: dict,
    active_object_id: str | None,
    animation_target: str | None,
    finished_object_ids: list[str],
    replay_token: str,
    key: str | None = None,
):
    background_path = COMPONENT_DIR / level["background"]
    if not background_path.exists():
        raise FileNotFoundError(f"Scene background not found: {background_path}")

    sprite_paths = KITCHEN_SPRITE_PATHS if level["id"] == "kitchen_01" else {}
    component_level = dict(level)
    component_level["active_object_id"] = active_object_id
    component_level["animation_target"] = animation_target
    component_level["finished_object_ids"] = finished_object_ids
    component_level["replay_token"] = replay_token
    component_level["background_data_url"] = _asset_data_url(
        str(background_path), background_path.stat().st_mtime_ns
    )
    component_level["sprite_data_urls"] = {
        name: _asset_data_url(str(path), path.stat().st_mtime_ns)
        for name, path in sprite_paths.items()
    }
    result = _scene_component(
        data=component_level,
        key=key,
        height="content",
        on_selected_change=lambda: None,
    )
    return result.selected
