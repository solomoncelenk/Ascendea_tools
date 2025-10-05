# Offer Ecosystem Map — Streamlit (Dark Mode)

Visualise **Entry → Core → Premium → Upsell → Recurring**, wire flows, and run financial diagnostics.

## Files
- `offer_ecosystem_app.py` — main app
- `requirements.txt` — dependencies
- `.streamlit/config.toml` — dark theme
- `offers_template.csv`, `flows_template.csv`, `errc_template.csv` — sample CSVs

## Deploy to Streamlit Community Cloud
1) Create a GitHub repo and upload all files from this folder.
2) Go to https://share.streamlit.io → New app.
3) Main file path: `offer_ecosystem_app.py` → Deploy.

## Local run
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run offer_ecosystem_app.py
```

### (Optional) Google Sheets
Add secrets in app settings → Secrets:
```
[gcp_service_account]
type = "service_account"
project_id = "<your-project>"
private_key_id = "<id>"
private_key = "-----BEGIN PRIVATE KEY-----
<key>
-----END PRIVATE KEY-----
"
client_email = "<svc>@<project>.iam.gserviceaccount.com"
client_id = "<id>"
token_uri = "https://oauth2.googleapis.com/token"

[gsheets]
url = "https://docs.google.com/spreadsheets/d/<YOUR_SHEET_ID>/edit#gid=0"
```
