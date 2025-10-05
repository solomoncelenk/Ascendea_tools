# Offer Profitability Toolkit — Expert Edition

### What you get
- **Streamlit App (dark mode)**: interactive analysis with uploads, schema mapping, Pareto, trends, waterfall, exports.
- **CLI Script**: batch run → CSVs + PNG charts saved to an output folder.

## Streamlit App
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run offer_profitability_app.py
```
Upload a CSV/XLSX (min columns: `offer,revenue,cogs`; optional: `date,segment,variable_costs,units`).

## CLI Script
```
python offer_profitability_cli.py   --input offers_sample.csv   --offer offer --revenue revenue --cogs cogs   --date date --segment segment --variable variable_costs --units units   --out output
```

Outputs:
- `output/summary.csv`
- `output/pareto_revenue.csv`
- `output/charts/*.png`

PNG export uses `kaleido`.
