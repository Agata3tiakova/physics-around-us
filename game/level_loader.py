import json
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent.parent
LEVELS_DIR = ROOT_DIR / "content" / "levels"
LEVEL_IDS = ("kitchen_01", "study_room_01")


@st.cache_data(show_spinner=False)
def _load_json(path_value: str, modified_ns: int):
    del modified_ns
    with Path(path_value).open("r", encoding="utf-8") as file:
        return json.load(file)


def _load_file(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Content not found: {path}")
    return _load_json(str(path), path.stat().st_mtime_ns)


def load_level(level_id: str) -> dict:
    return _load_file(LEVELS_DIR / f"{level_id}.json")


def load_levels() -> list[dict]:
    return [load_level(level_id) for level_id in LEVEL_IDS]


def load_formulas() -> list[dict]:
    return _load_file(ROOT_DIR / "content" / "formulas.json")
