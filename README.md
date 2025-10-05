# Blue Ocean Strategy Canvas — Streamlit (Dark Mode)

This app lets you:
- Define buyer value factors and score your offer vs competitors.
- Visualise a Strategy Canvas (line chart).
- Build an ERRC grid (Eliminate/Reduce/Raise/Create) with auto-suggestions.
- Generate a narrative Offer Differentiation Report.

## Files
- `blue_ocean_app.py` — main app
- `requirements.txt` — dependencies
- `.streamlit/config.toml` — dark theme
- `strategy_canvas_template.csv` — sample CSV (wide format)

## Deploy to Streamlit Community Cloud
1. Create a GitHub repo and upload all files from this folder.
2. Go to https://share.streamlit.io → Sign in → New app.
3. Set **Main file path** to `blue_ocean_app.py` and Deploy.

## Local run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run blue_ocean_app.py
```
