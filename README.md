# Physics Around Us

An interactive educational game for discovering physics in illustrated everyday scenes. Players inspect animated objects, identify every applicable physical process, connect observations to formulas, and review step-by-step explanations.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://physics-around-us-agata3tiakova.streamlit.app/)

**Live app:** [physics-around-us-agata3tiakova.streamlit.app](https://physics-around-us-agata3tiakova.streamlit.app/)

## Current Levels

1. **Physics in the Kitchen** - mechanics, heat transfer, convection, phase changes, and electrical power.
2. **Study Room** - reflection, refraction, image formation, dispersion, and electrical energy.

Each level includes five observable phenomena, multi-select answers, hints, scoring, replayable animations, and a notebook-style learning summary.

## Technology

- Streamlit and Python for navigation, game state, validation, and scoring.
- HTML, CSS, and JavaScript for the interactive scenes and animations.
- JSON files for level content and formula definitions.
- Layered watercolor assets for scene backgrounds and interactive objects.

## Run Locally

Python 3.11 or newer is recommended.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in a browser.

## Project Structure

```text
app.py                  Streamlit entry point and navigation
pages/                  Home, level, and result views
game/                   State, scoring, validation, and content loading
components/scene/       Interactive scene component
content/levels/         JSON level definitions
content/formulas.json   Formula library and explanations
assets/                 Shared artwork and interface styling
.streamlit/config.toml  Streamlit client and theme configuration
```

## Progress Storage

The current prototype stores progress in `st.session_state`. Progress is retained while the browser session is active but is not yet persisted between separate sessions.
