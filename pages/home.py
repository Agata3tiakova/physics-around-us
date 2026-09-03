import streamlit as st
from textwrap import dedent

from game.level_loader import load_level
from game.state import initialize_state, reset_level
from game.ui import apply_global_styles, render_level_navigation, ui_asset_data_uri


initialize_state()
apply_global_styles()

level = load_level(st.session_state.current_level)
completed = len(st.session_state.found_objects)
total = len(level["objects"])

with st.sidebar:
    st.markdown("### Physics Around Us")
    st.caption("Interactive learning prototype")
    st.divider()
    render_level_navigation()
    st.divider()
    st.metric("Current level progress", f"{completed}/{total}")
    st.progress(completed / total if total else 0)
    if st.button("Restart", use_container_width=True, icon=":material/restart_alt:"):
        reset_level()
        st.rerun()

sections = [
    (
        "Mechanics",
        "Track how forces change motion and how energy moves between objects.",
        "topic-mechanics.png",
        True,
    ),
    (
        "Thermodynamics",
        "Follow heat as it warms matter, flows, and changes its state.",
        "topic-thermodynamics-solid.png",
        True,
    ),
    (
        "Electricity",
        "Connect current and voltage to power and energy transformations.",
        "topic-electricity.png",
        True,
    ),
    (
        "Optics",
        "Trace light to explain reflection, refraction, and image formation.",
        "topic-optics-solid.png",
        True,
    ),
]
cloud_uri = ui_asset_data_uri("topic-cloud.png")

topic_clouds = []
for title, description, artwork, available in sections:
    status = "Available" if available else "Coming soon"
    status_class = "is-available" if available else "is-locked"
    image_uri = ui_asset_data_uri(artwork)
    topic_clouds.append(
        dedent(f"""
        <article class="topic-cloud topic-cloud--{title.lower()} {status_class}" aria-label="{title}: {description}. {status}.">
            <img class="topic-cloud__background" src="{cloud_uri}" alt="" />
            <div class="topic-cloud__content">
                <img src="{image_uri}" alt="" />
                <div class="topic-cloud__copy">
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
            </div>
        </article>
        """)
    )

home_markup = (
    '<div class="home-page-marker"></div>'
    '<section class="home-hero">'
    '<div class="home-hero__copy">'
    '<p class="home-eyebrow">Observation lab</p>'
    '<h1>Physics Around Us</h1>'
    '<p>Discover physical phenomena in everyday scenes and connect each observation to the laws that explain it.</p>'
    '</div>'
    '</section>'
    '<section class="home-topics" aria-labelledby="topics-title">'
    '<h2 id="topics-title">Topics</h2>'
    f'<div class="topic-cloud-grid">{"".join(topic_clouds)}</div>'
    '</section>'
    '<section class="home-observation-note" aria-labelledby="observation-method-title">'
    '<div class="home-observation-note__binding" aria-hidden="true"></div>'
    '<div class="home-observation-note__content">'
    '<p class="home-observation-note__label">Investigator’s notebook</p>'
    '<h2 id="observation-method-title">How to read a scene</h2>'
    '<p class="home-observation-note__intro">Every level is an investigation. A single event can show several physical processes, so look for every law that helps explain it.</p>'
    '<ol class="observation-steps">'
    '<li><span>1</span><div><strong>Notice</strong><p>What is moving, warming, glowing, flowing, or changing?</p></div></li>'
    '<li><span>2</span><div><strong>Name</strong><p>Identify the processes responsible for the change you observed.</p></div></li>'
    '<li><span>3</span><div><strong>Connect</strong><p>Choose every formula that describes those processes.</p></div></li>'
    '</ol>'
    '</div>'
    '</section>'
)
st.markdown(home_markup, unsafe_allow_html=True)

st.markdown('<div class="current-level-marker"><h2>Current Level</h2></div>', unsafe_allow_html=True)
left, right = st.columns([3, 1])
with left:
    st.markdown(f"### Level {level['number']} · {level['title']}")
    st.write(level["description"])
    st.caption(f"{total} phenomena · {len(level['formula_ids'])} formulas")
with right:
    if st.button("Continue", type="primary", use_container_width=True, icon=":material/play_arrow:"):
        st.switch_page("pages/level.py")
