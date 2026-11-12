# Physics Around Us

An interactive educational game for discovering physics in illustrated everyday scenes. Players inspect animated objects, identify every applicable physical process, connect observations to formulas, and review step-by-step explanations.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://physics-around-us-agata3tiakova.streamlit.app/)

**Live app:** [physics-around-us-agata3tiakova.streamlit.app](https://physics-around-us-agata3tiakova.streamlit.app/)

## Current Levels

1. **Physics in the Kitchen** - mechanics, heat transfer, convection, phase changes, and electrical power.
2. **Study Room** - reflection, refraction, image formation, dispersion, and electrical energy.

Each level includes five clickable phenomena, multi-select answers, hints, scoring, and a notebook-style learning summary. You can switch directly between levels in the sidebar and reopen it after collapsing it.

- **Kitchen:** falling box, jumping cat, heating soup, rising steam, and an electric kettle. Use **Play scene** or an object's **Replay animation** button. The box lands on the countertop and the cat sits on it; animations do not loop automatically.
- **Study Room:** desk lamp, table mirror, paintbrush in water, magnifying glass, and a prism.
- **Answers:** select every applicable process and formula without extra selections. Results show the status and score; correct answers, reasoning, and formula notes are inside **Show complete explanation**.

## Technology

- Streamlit and Python for navigation, game state, validation, and scoring.
- HTML, CSS, and JavaScript for the interactive scenes and animations.
- JSON files for level content and formula definitions.
- Hand-drawn scene artwork, with transparent PNG layers for kitchen objects.

## Run Locally

Use Python 3.12 or newer (tested with Python 3.13). Streamlit is pinned to the tested version in `requirements.txt`; the interactive scene uses the components v2 API.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open `http://localhost:8501` in a browser.

If that port is already in use, add `--server.port=8503` to the launch command and open `http://localhost:8503`. Local ports do not change the public Streamlit Cloud URL.

## Tests

From the project root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests cover content references, level loading and reruns, kitchen controls, legacy level links, and keeping answer explanations inside the results expander. Browser checks are still needed for animation timing, visual alignment, and responsive layout.

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
tests/                  Content checks and Streamlit AppTest regression tests
```

## Progress Storage

The current prototype stores progress in `st.session_state`. Progress is retained while the browser session is active but is not yet persisted between separate sessions.

There is no database or login. Refreshing or disconnecting can reset progress. Artwork and JSON loads are cached using file modification times; scene CSS and JavaScript use content-versioned component names.

## Deployment And Troubleshooting

The public app is hosted on Streamlit Community Cloud, not GitHub Pages. Its source is the `main` branch of [Agata3tiakova/physics-around-us](https://github.com/Agata3tiakova/physics-around-us), with `app.py` as the entry point. Committing locally does not update the site; changes must be pushed to GitHub.

If a running server still refers to removed content after an update, restart the local Streamlit process or reboot the Cloud app. Errors are hidden from visitors; inspect the terminal locally or the Cloud application's logs for the actual traceback.
