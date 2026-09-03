from html import escape

import streamlit as st

from game.level_loader import load_formulas, load_level
from game.state import initialize_state, select_level
from game.ui import apply_global_styles, render_level_navigation


initialize_state()
apply_global_styles()
level = load_level(st.session_state.current_level)
formulas = load_formulas()
result = st.session_state.last_result
process_by_id = {item["id"]: item["label"] for item in level["processes"]}
formula_by_id = {
    item["id"]: f"{item['name']} · {item['expression']}" for item in formulas
}
formula_data_by_id = {item["id"]: item for item in formulas}

st.markdown(
    f'<div class="level-theme-marker level-theme--{level["id"]}"></div>',
    unsafe_allow_html=True,
)


def labels(ids: list[str], source: dict[str, str]) -> str:
    return ", ".join(source[item] for item in ids) if ids else "None"


with st.sidebar:
    st.markdown("### Physics Around Us")
    st.caption(f"Level {level['number']} results")
    st.divider()
    if st.button("Home", use_container_width=True, icon=":material/home:"):
        st.switch_page("pages/home.py")
    st.divider()
    render_level_navigation()
    st.divider()
    st.metric("Score", st.session_state.score)
    st.metric("Found", f"{len(st.session_state.found_objects)}/{len(level['objects'])}")

if not result:
    st.info("Choose a phenomenon on the level before viewing results.")
    if st.button("Back to level", icon=":material/arrow_back:"):
        st.switch_page("pages/level.py")
    st.stop()

st.markdown('<div class="page-kicker">Answer review</div>', unsafe_allow_html=True)
st.title("Observation Results")
if result["is_fully_correct"]:
    st.success("You selected every applicable process and formula.", icon=":material/check_circle:")
elif result["process_correct"] or result["formula_correct"]:
    st.warning("One part is complete; the other still has missing or extra options.", icon=":material/warning:")
else:
    st.error("The answer is incomplete or contains extra options.", icon=":material/error:")

st.metric("Best score for this object", f"{st.session_state.object_scores.get(result['object_id'], 0)} points")
hint_status = "used" if result["hint_used"] else "not used"
st.caption(f"Attempt: {result['attempts']} · Hint: {hint_status}")
st.markdown(f"## {result['object_label']}")
st.write(result["explanation"])

reasoning_steps = result.get("reasoning_steps", [])
if reasoning_steps:
    reasoning_items = "".join(
        f"<li><span>{index}</span><p>{escape(step)}</p></li>"
        for index, step in enumerate(reasoning_steps, start=1)
    )
    st.markdown(
        '<section class="reasoning-note" aria-labelledby="reasoning-title">'
        '<div class="reasoning-note__label">Observation notes</div>'
        '<h2 id="reasoning-title">Why this happens</h2>'
        f'<ol>{reasoning_items}</ol>'
        '</section>',
        unsafe_allow_html=True,
    )

formula_cards = []
for formula_id in result["correct_formula_ids"]:
    formula = formula_data_by_id.get(formula_id)
    if not formula:
        continue
    formula_cards.append(
        '<article class="formula-note">'
        f'<div class="formula-note__name">{escape(formula["name"])}</div>'
        f'<div class="formula-note__expression">{escape(formula["expression"])}</div>'
        f'<p>{escape(formula.get("meaning", ""))}</p>'
        '</article>'
    )
if formula_cards:
    st.markdown("## Formula Notes")
    st.markdown(
        f'<div class="formula-note-grid">{"".join(formula_cards)}</div>',
        unsafe_allow_html=True,
    )

st.markdown("## Answer Details")
status_columns = st.columns(2)
with status_columns[0]:
    st.markdown("### Processes")
    if result["process_correct"]:
        st.success("Complete set")
    else:
        st.warning("Needs revision")
    st.caption("Selected: " + labels(result["selected_process_ids"], process_by_id))
with status_columns[1]:
    st.markdown("### Formulas")
    if result["formula_correct"]:
        st.success("Complete set")
    else:
        st.warning("Needs revision")
    st.caption("Selected: " + labels(result["selected_formula_ids"], formula_by_id))

if not result["is_fully_correct"]:
    with st.expander("Show complete explanation"):
        st.write("Correct processes: " + labels(result["correct_process_ids"], process_by_id))
        st.write("Correct formulas: " + labels(result["correct_formula_ids"], formula_by_id))
        if result["extra_process_ids"] or result["extra_formula_ids"]:
            st.caption("Your answer included extra options; remove them as well.")

level_complete = len(st.session_state.found_objects) == len(level["objects"])
if level_complete:
    st.balloons()
    st.success(
        f"You found every phenomenon in {level['title']}. Level {level['number']} is complete.",
        icon=":material/trophy:",
    )

home_column, retry_column, next_column = st.columns(3)
with home_column:
    if st.button("Home", use_container_width=True, icon=":material/home:", key="result-home"):
        st.switch_page("pages/home.py")
with retry_column:
    retry_label = "Try Again" if not result["is_fully_correct"] else "Return to Scene"
    if st.button(retry_label, use_container_width=True, icon=":material/replay:"):
        st.session_state.last_result = None
        st.switch_page("pages/level.py")
with next_column:
    next_level_id = level.get("next_level") if level_complete else None
    next_label = "Next Level" if next_level_id else "Next Object"
    if st.button(next_label, type="primary", use_container_width=True, icon=":material/play_arrow:"):
        if next_level_id:
            st.query_params["level"] = next_level_id
            select_level(next_level_id)
        else:
            st.session_state.selected_object = None
            st.session_state.last_result = None
        st.switch_page("pages/level.py")
