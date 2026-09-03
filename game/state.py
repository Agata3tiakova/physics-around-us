import streamlit as st


LEVEL_STATE_KEYS = (
    "selected_object",
    "found_objects",
    "answers",
    "score",
    "hints_used",
    "hinted_objects",
    "attempts",
    "object_scores",
    "last_result",
    "scene_replay_token",
    "scene_animation_target",
    "scene_finished_objects",
    "last_scene_event_token",
)


def initialize_state() -> None:
    defaults = {
        "current_level": "kitchen_01",
        "selected_object": None,
        "found_objects": [],
        "answers": {},
        "score": 0,
        "hints_used": 0,
        "hinted_objects": [],
        "attempts": {},
        "object_scores": {},
        "last_result": None,
        "scene_replay_token": "0",
        "scene_animation_target": None,
        "scene_finished_objects": [],
        "last_scene_event_token": "0",
        "level_states": {},
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_level() -> None:
    st.session_state.selected_object = None
    st.session_state.found_objects = []
    st.session_state.answers = {}
    st.session_state.score = 0
    st.session_state.hints_used = 0
    st.session_state.hinted_objects = []
    st.session_state.attempts = {}
    st.session_state.object_scores = {}
    st.session_state.last_result = None
    st.session_state.scene_replay_token = "0"
    st.session_state.scene_animation_target = None
    st.session_state.scene_finished_objects = []
    st.session_state.last_scene_event_token = "0"


def select_level(level_id: str) -> None:
    current_level = st.session_state.current_level
    if level_id == current_level:
        return

    st.session_state.level_states[current_level] = {
        key: st.session_state[key] for key in LEVEL_STATE_KEYS
    }
    st.session_state.current_level = level_id
    saved_state = st.session_state.level_states.get(level_id)
    reset_level()
    if saved_state:
        for key, value in saved_state.items():
            st.session_state[key] = value