# Obviously Awesome Positioning Canvas — Streamlit (Dark Mode)

This app helps you implement April Dunford's framework:
- **Competitive Alternatives**, **Unique Attributes**, **Value Themes**, **ICP**, **Market Category**, **Narrative Check**
- **Differentiator Scorecard** with adjustable weights
- **Positioning Statement** builder
- **PNG downloads** (scorecard + scatter)
- **Google Sheets** load/save (optional)

## Deploy (Streamlit Community Cloud)
1) Push these files to a GitHub repo.
2) On Streamlit Cloud → New app → Main file: `dunford_positioning_app.py` → Deploy.

### Google Sheets secrets (optional)
In app settings → Secrets:
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

## Local run
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run dunford_positioning_app.py
```
