from time import time_ns
from html import escape

import streamlit as st

from components.scene import physics_scene
from game.level_loader import load_formulas, load_level
from game.state import initialize_state, reset_level
from game.ui import apply_global_styles, render_level_navigation
from game.validators import validate_answer


initialize_state()
apply_global_styles()
level = load_level(st.session_state.current_level)
animated_object_ids = set(level.get("animated_object_ids", []))
formulas = load_formulas()
formula_by_id = {formula["id"]: formula for formula in formulas}
object_by_id = {item["id"]: item for item in level["objects"]}

st.markdown(
    f'<div class="level-theme-marker level-theme--{level["id"]}"></div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Physics Around Us")
    st.caption(f"Level {level['number']} · {level['title']}")
    st.divider()
    if st.button("Home", use_container_width=True, icon=":material/home:"):
        st.switch_page("pages/home.py")
    st.divider()
    render_level_navigation()
    st.divider()
    st.metric("Found", f"{len(st.session_state.found_objects)}/{len(level['objects'])}")
    st.progress(len(st.session_state.found_objects) / len(level["objects"]))
    st.metric("Score", st.session_state.score)
    st.caption(f"Hints used: {st.session_state.hints_used}")
    st.divider()
    if st.button("Restart level", use_container_width=True, icon=":material/restart_alt:"):
        reset_level()
        st.rerun()

st.markdown(
    f'<div class="page-kicker">Level {level["number"]} · {level["kicker"]}</div>',
    unsafe_allow_html=True,
)
st.title(level["page_title"])
st.markdown(
    '<p class="page-lead">Select an object, then identify every process and formula that applies to it.</p>',
    unsafe_allow_html=True,
)

learning_points = "".join(
    f"<li>{escape(point)}</li>" for point in level.get("learning_points", [])
)
if level.get("learning_summary"):
    st.markdown(
        f"""
        <section class="learning-focus" aria-labelledby="learning-focus-title">
            <div class="learning-focus__binding" aria-hidden="true"></div>
            <div class="learning-focus__content">
                <div class="learning-focus__label">
                    <span>Scene notebook</span>
                    <span>Level {level["number"]} field notes</span>
                </div>
                <h2 id="learning-focus-title">Ideas to watch for</h2>
                <p>{escape(level["learning_summary"])}</p>
                <ul>{learning_points}</ul>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

if animated_object_ids:
    play_column, _ = st.columns([1.2, 4])
    with play_column:
        if st.button("Play scene", type="primary", use_container_width=True, icon=":material/play_arrow:"):
            st.session_state.scene_animation_target = "all"
            st.session_state.scene_finished_objects = sorted(animated_object_ids)
            st.session_state.scene_replay_token = f"{time_ns()}-all"
            st.rerun()

scene_event = physics_scene(
    level,
    active_object_id=st.session_state.selected_object,
    animation_target=st.session_state.get("scene_animation_target"),
    finished_object_ids=st.session_state.get("scene_finished_objects", []),
    replay_token=st.session_state.scene_replay_token,
    key=f"physics-scene-{level['id']}",
)
if isinstance(scene_event, dict):
    event_token = str(scene_event.get("replay_token", ""))
    object_id = scene_event.get("object_id")
    if object_id in object_by_id and event_token and event_token != st.session_state.last_scene_event_token:
        st.session_state.selected_object = object_id
        st.session_state.last_scene_event_token = event_token
        st.rerun()

selected_object_id = st.session_state.selected_object
if selected_object_id not in object_by_id:
    st.info("Select an object in the scene to begin your observation.")
    st.stop()

selected_object = object_by_id[selected_object_id]
st.markdown('<div class="page-kicker">Selected phenomenon</div>', unsafe_allow_html=True)
st.markdown(f"## {selected_object['label']}")
st.write(selected_object["prompt"])

if selected_object_id in animated_object_ids:
    action_left, action_replay, action_hint, _ = st.columns([1.15, 1.15, .85, 2])
else:
    action_left, action_hint, _ = st.columns([1.15, .85, 3.15])
    action_replay = None

with action_left:
    if st.button("Choose another", use_container_width=True, icon=":material/ads_click:"):
        st.session_state.selected_object = None
        st.rerun()

if action_replay is not None:
    with action_replay:
        if st.button("Replay animation", use_container_width=True, icon=":material/replay:"):
            st.session_state.scene_animation_target = selected_object_id
            st.session_state.scene_finished_objects = sorted(
                set(st.session_state.get("scene_finished_objects", [])) | {selected_object_id}
            )
            st.session_state.scene_replay_token = f"{time_ns()}-{selected_object_id}"
            st.rerun()
with action_hint:
    if st.button("Hint", use_container_width=True, icon=":material/lightbulb:"):
        if selected_object_id not in st.session_state.hinted_objects:
            st.session_state.hinted_objects.append(selected_object_id)
            st.session_state.hints_used += 1

if selected_object_id in st.session_state.hinted_objects:
    st.info(selected_object["hint"], icon=":material/lightbulb:")

process_options = {process["label"]: process["id"] for process in level["processes"]}
formula_options = {
    f"{formula_by_id[item]['name']} · {formula_by_id[item]['expression']}": item
    for item in level["formula_ids"]
    if item in formula_by_id
}

st.markdown("## Build Your Answer")
with st.form(f"answer-{selected_object_id}"):
    process_labels = st.multiselect(
        "Which processes are taking place?",
        list(process_options),
        placeholder="Select one or more processes",
        key=f"processes-{level['id']}-{selected_object_id}",
    )
    formula_labels = st.multiselect(
        "Which formulas apply?",
        list(formula_options),
        placeholder="Select every applicable formula",
        key=f"formulas-{level['id']}-{selected_object_id}",
    )
    st.caption("Your answer is correct only when every applicable option is selected and no extra options remain.")
    submitted = st.form_submit_button(
        "Check Answer",
        type="primary",
        use_container_width=True,
        icon=":material/check:",
    )

if submitted:
    if not process_labels or not formula_labels:
        st.warning("Select at least one process and one formula.", icon=":material/warning:")
        st.stop()

    attempts = st.session_state.attempts.get(selected_object_id, 0) + 1
    st.session_state.attempts[selected_object_id] = attempts
    result = validate_answer(
        level=level,
        object_id=selected_object_id,
        selected_process_ids=[process_options[label] for label in process_labels],
        selected_formula_ids=[formula_options[label] for label in formula_labels],
        attempts=attempts,
        hint_used=selected_object_id in st.session_state.hinted_objects,
    )
    st.session_state.answers[selected_object_id] = result

    previous_award = st.session_state.object_scores.get(selected_object_id, 0)
    new_award = max(previous_award, result["score"])
    st.session_state.score += new_award - previous_award
    st.session_state.object_scores[selected_object_id] = new_award

    if result["is_fully_correct"] and selected_object_id not in st.session_state.found_objects:
        st.session_state.found_objects.append(selected_object_id)

    st.session_state.last_result = result
    st.switch_page("pages/results.py")
