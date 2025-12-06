# Value Equation App (Ascendea UI) – Themed, High-Contrast, Branded Chart

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

# ---------- Theme Tokens ----------
DARK_TOKENS = {
    "PRIMARY": "#ffffff",
    "MUTED": "rgba(57,57,60,0.78)",
    "DISABLED": "rgba(57,57,60,0.45)",
    "BG": "#050814",
}

LIGHT_TOKENS = {
    "PRIMARY": "#0b1020",
    "MUTED": "#4b5563",
    "DISABLED": "#9ca3af",
    "BG": "#f5f7fb",
}

st.set_page_config(
    page_title="Ascendea - Value Equation Calculator",
    page_icon="📈",
    layout="wide",
)

# ---------- Sidebar: Theme + Weights ----------
st.sidebar.header("Display & Weights")

theme_choice = st.sidebar.radio("Theme", ["Dark", "Light"], index=0, horizontal=True)

TOKENS = DARK_TOKENS if theme_choice == "Dark" else LIGHT_TOKENS

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Factor Weights")
st.sidebar.caption("1.0 = neutral. Adjust weights to match your market reality.")

w_outcome = st.sidebar.slider("Dream Outcome weight", 0.2, 3.0, 1.0, 0.1)
w_likelihood = st.sidebar.slider("Likelihood weight", 0.2, 3.0, 1.0, 0.1)
w_time = st.sidebar.slider("Time Delay penalty", 0.2, 3.0, 1.0, 0.1)
w_effort = st.sidebar.slider("Effort & Sacrifice penalty", 0.2, 3.0, 1.0, 0.1)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Lower Time Delay and Effort & Sacrifice scores mean less friction. "
    "If your data inverts that meaning, normalise before upload."
)

# ---------- CSS per Theme ----------
DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="stApp"] {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  color: #ffffff;
}

.stApp {
  background: #000000;
}

.main {
  background:
    radial-gradient(circle at 10% 0%, rgba(78,191,176,0.35) 0, transparent 45%),
    radial-gradient(circle at 90% 100%, rgba(238,65,40,0.35) 0, transparent 55%),
    radial-gradient(circle at 50% 20%, #151a30 0, #050814 60%, #000000 100%);
}

.block-container {
  max-width: 1120px;
  padding-top: 2.5rem;
  padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(160deg, #050814 0%, #090f1f 40%, #141a32 100%);
  border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * {
  color: #ffffff;
}

/* Cards */
.asc-card {
  border-radius: 24px;
  border: 1px solid rgba(255,255,255,0.18);
  background:
    radial-gradient(circle at 0% 0%, rgba(78,191,176,0.18) 0, transparent 50%),
    radial-gradient(circle at 100% 100%, rgba(238,65,40,0.18) 0, transparent 50%),
    rgba(7,10,24,0.96);
  padding: 1.5rem 1.75rem;
  box-shadow:
    0 26px 90px rgba(0,0,0,0.85),
    0 0 0 1px rgba(255,255,255,0.02);
  margin-bottom: 1.5rem;
}

/* Typography */
.asc-eyebrow {
  font-size: 0.78rem;
  letter-spacing: 0.26em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.9);
}

.asc-title {
  font-size: 1.9rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-top: 0.35rem;
  margin-bottom: 0.4rem;
  color: #ffffff;
}

.asc-title span {
  color: #4ebfb0;
}

.asc-subtitle {
  font-size: 0.98rem;
  color: rgba(255,255,255,0.78);
  max-width: 720px;
}

/* Dataframes */
.dataframe tbody tr th {
  color: #ffffff;
}

.dataframe thead th {
  background: rgba(11,16,35,0.9);
  color: #ffffff;
}

.dataframe tbody tr:nth-child(even) {
  background: rgba(6,9,24,0.85);
}

.dataframe tbody tr:nth-child(odd) {
  background: rgba(9,13,28,0.95);
}

.dataframe td, .dataframe th {
  border-color: rgba(255,255,255,0.12) !important;
}

/* Download / buttons */
.asc-download-wrap {
  margin-top: 0.75rem;
}

/* Ascendea button styling */
.stButton > button, .stDownloadButton > button {
  background: #00E4AB !important;
  color: #393939 !important;
  border: 1px solid #FFFDD1 !important;
  border-radius: 999px;
  padding: 0.45rem 1.2rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.stButton > button:hover, .stDownloadButton > button:hover {
  filter: brightness(1.05);
  box-shadow: 0 14px 40px rgba(0,0,0,0.45);
}

/* General text contrast */
h1, h2, h3, h4, h5, h6, p, span, label {
  color: #ffffff;
}

/* Mobile */
@media (max-width: 900px) {
  .block-container {
    padding-left: 1.0rem;
    padding-right: 1.0rem;
  }
  .asc-card {
    padding: 1.1rem 1.1rem;
  }
  .asc-title {
    font-size: 1.4rem;
  }
  .asc-subtitle {
    font-size: 0.9rem;
  }
}
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="stApp"] {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  color: #0b1020;
}

.stApp {
  background: #e5ebf5;
}

.main {
  background: linear-gradient(145deg, #eef2ff 0%, #f5f7fb 40%, #e5ebf5 100%);
}

.block-container {
  max-width: 1120px;
  padding-top: 2.5rem;
  padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: #ffffff;
  border-right: 1px solid rgba(15,23,42,0.08);
}
section[data-testid="stSidebar"] * {
  color: #111827;
}

/* Cards */
.asc-card {
  border-radius: 24px;
  border: 1px solid rgba(15,23,42,0.06);
  background: radial-gradient(circle at 0% 0%, rgba(78,191,176,0.14) 0, transparent 50%),
              radial-gradient(circle at 100% 100%, rgba(238,65,40,0.14) 0, transparent 50%),
              #ffffff;
  padding: 1.5rem 1.75rem;
  box-shadow:
    0 18px 60px rgba(15,23,42,0.15),
    0 0 0 1px rgba(15,23,42,0.02);
  margin-bottom: 1.5rem;
}

/* Typography */
.asc-eyebrow {
  font-size: 0.78rem;
  letter-spacing: 0.26em;
  text-transform: uppercase;
  color: #4b5563;
}

.asc-title {
  font-size: 1.9rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-top: 0.35rem;
  margin-bottom: 0.4rem;
  color: #0b1020;
}

.asc-title span {
  color: #059669;
}

.asc-subtitle {
  font-size: 0.98rem;
  color: #4b5563;
  max-width: 720px;
}

/* Dataframes */
.dataframe tbody tr th {
  color: #111827;
}

.dataframe thead th {
  background: #f3f4f6;
  color: #111827;
}

.dataframe tbody tr:nth-child(even) {
  background: #f9fafb;
}

.dataframe tbody tr:nth-child(odd) {
  background: #ffffff;
}

.dataframe td, .dataframe th {
  border-color: rgba(15,23,42,0.08) !important;
}

/* Download / buttons */
.asc-download-wrap {
  margin-top: 0.75rem;
}

/* Ascendea button styling */
.stButton > button, .stDownloadButton > button {
  background: #00E4AB !important;
  color: #393939 !important;
  border: 1px solid #FFFDD1 !important;
  border-radius: 999px;
  padding: 0.45rem 1.2rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  box-shadow: 0 10px 30px rgba(15,23,42,0.25);
}
.stButton > button:hover, .stDownloadButton > button:hover {
  filter: brightness(1.03);
  box-shadow: 0 14px 40px rgba(15,23,42,0.35);
}

/* General text contrast */
h1, h2, h3, h4, h5, h6, p, span, label {
  color: #0b1020;
}

/* Mobile */
@media (max-width: 900px) {
  .block-container {
    padding-left: 1.0rem;
    padding-right: 1.0rem;
  }
  .asc-card {
    padding: 1.1rem 1.1rem;
  }
  .asc-title {
    font-size: 1.4rem;
  }
  .asc-subtitle {
    font-size: 0.9rem;
  }
}
</style>
"""

st.markdown(DARK_CSS if theme_choice == "Dark" else LIGHT_CSS, unsafe_allow_html=True)

# ---------- Data helpers ----------
REQUIRED_COLS = ["offer", "dream_outcome", "likelihood", "time_delay", "effort_sacrifice"]
OPTIONAL_COLS = ["group"]

def canonicalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "offer": "offer",
        "name": "offer",
        "dream outcome": "dream_outcome",
        "dream_outcome": "dream_outcome",
        "outcome": "dream_outcome",
        "likelihood": "likelihood",
        "pol": "likelihood",
        "probability": "likelihood",
        "time delay": "time_delay",
        "time_delay": "time_delay",
        "time": "time_delay",
        "effort & sacrifice": "effort_sacrifice",
        "effort_sacrifice": "effort_sacrifice",
        "effort": "effort_sacrifice",
        "group": "group",
        "segment": "group",
        "competitor": "group",
    }
    df = df.copy()
    df.columns = [c.strip().lower().replace("-", "_").replace(" ", "_") for c in df.columns]
    df.rename(columns={c: mapping.get(c, c) for c in df.columns}, inplace=True)
    return df

def coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def validate_required_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in REQUIRED_COLS if c not in df.columns]

def compute_value_score(
    df: pd.DataFrame,
    w_outcome: float = 1.0,
    w_likelihood: float = 1.0,
    w_time: float = 1.0,
    w_effort: float = 1.0,
) -> pd.DataFrame:
    df = df.copy()
    for col in ["dream_outcome", "likelihood", "time_delay", "effort_sacrifice"]:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)

    num = (
        df["dream_outcome"].clip(lower=1e-9) ** w_outcome
        * df["likelihood"].clip(lower=1e-9) ** w_likelihood
    )
    den = (
        df["time_delay"].clip(lower=1e-9) ** w_time
        * df["effort_sacrifice"].clip(lower=1e-9) ** w_effort
    )

    df["value_score"] = num / den
    return df

def starter_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "offer": ["Core Coaching", "Premium Sprint", "Enterprise Advisory"],
            "dream_outcome": [8, 10, 10],
            "likelihood": [7, 8, 9],
            "time_delay": [6, 4, 3],
            "effort_sacrifice": [5, 4, 3],
            "group": ["Company", "Company", "Company"],
        }
    )

def clean_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    df = canonicalize_columns(df)
    miss = validate_required_columns(df)
    if miss:
        raise ValueError("Missing required columns: " + ", ".join(miss))

    keep = [c for c in REQUIRED_COLS + OPTIONAL_COLS if c in df.columns]
    df = df[keep].copy()

    df = coerce_numeric(df, [c for c in REQUIRED_COLS if c != "offer"])

    for c in ["dream_outcome", "likelihood", "time_delay", "effort_sacrifice"]:
        df[c] = df[c].clip(lower=0.1, upper=10)

    if "group" not in df.columns:
        df["group"] = "Company"

    df["offer"] = df["offer"].astype(str).str.strip()
    return df

def download_csv_button(df: pd.DataFrame, filename: str = "value_equation_results.csv"):
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    with st.container():
        st.markdown('<div class="asc-download-wrap">', unsafe_allow_html=True)
        st.download_button(
            "📥 Download results (CSV)",
            data=csv_bytes,
            file_name=filename,
            mime="text/csv",
        )
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- Header + Intro ----------
st.markdown(
    """
    <div class="asc-card">
      <div class="asc-eyebrow">Ascendea Value Architecture</div>
      <div class="asc-title">The <span>Value Equation</span> Calculator</div>
      <div class="asc-subtitle">
        This simulator ranks every offer on perceived value – how big the outcome is,
        how likely it is to happen, and how much time and effort it really costs your buyer.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="asc-card">
      <div class="asc-eyebrow">How this equation works</div>
      <div class="asc-subtitle" style="margin-top:0.5rem;">
        <strong>Value Equation</strong> =
        (Dream Outcome × Likelihood of Achievement) ÷ (Time Delay × Effort & Sacrifice).
        <br/><br/>
        • Increase perceived value by raising <strong>Dream Outcome</strong> and <strong>Likelihood</strong>.<br/>
        • Increase perceived value by reducing <strong>Time Delay</strong> and <strong>Effort & Sacrifice</strong>.<br/>
        • Use the weights in the sidebar when your market is more sensitive to speed, certainty, or friction.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Data ingest ----------
with st.container():
    upload_col, _ = st.columns([3, 2])
    with upload_col:
        st.markdown("#### 1. Load your offers")
        uploaded = st.file_uploader(
            "Upload CSV (offer, dream_outcome, likelihood, time_delay, effort_sacrifice, [group])",
            type=["csv"],
        )

if uploaded is not None:
    try:
        raw = pd.read_csv(uploaded)
        df_in = clean_and_prepare(raw)
        st.success("CSV loaded successfully.")
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()
else:
    st.info("No CSV uploaded. Using the starter offers below.")
    df_in = starter_dataframe()

# ---------- Edit / review ----------
st.markdown(
    """
    <div class="asc-eyebrow" style="margin-top:1.25rem;">Step 2</div>
    <h3 style="margin-top:0.25rem;">Review and edit your inputs</h3>
    <p style="font-size:0.95rem;">
      Keep everything on a 1–10 scale. Higher is better for outcome and likelihood.
      Lower is better for time and effort.
    </p>
    """,
    unsafe_allow_html=True,
)

edited = st.data_editor(
    df_in,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "offer": st.column_config.TextColumn("Offer", help="Name of the offer / product / package"),
        "dream_outcome": st.column_config.NumberColumn("Dream Outcome (1–10)"),
        "likelihood": st.column_config.NumberColumn("Likelihood (1–10)"),
        "time_delay": st.column_config.NumberColumn("Time Delay (1–10, lower = better)"),
        "effort_sacrifice": st.column_config.NumberColumn("Effort & Sacrifice (1–10, lower = better)"),
        "group": st.column_config.TextColumn("Group (optional, e.g. Company vs Competitor)"),
    },
)

try:
    df_clean = clean_and_prepare(edited)
except Exception as e:
    st.error(f"Data validation error: {e}")
    st.stop()

# ---------- Compute ----------
df_scored = compute_value_score(
    df_clean,
    w_outcome=w_outcome,
    w_likelihood=w_likelihood,
    w_time=w_time,
    w_effort=w_effort,
)

df_scored["rank"] = df_scored["value_score"].rank(ascending=False, method="dense").astype(int)
df_scored = df_scored.sort_values(["rank", "value_score"], ascending=[True, False]).reset_index(drop=True)

# ---------- Outputs: table ----------
st.markdown("#### 3. Ranked value scores")
st.caption("Higher scores indicate higher perceived value after friction.")

st.dataframe(
    df_scored[
        [
            "rank",
            "offer",
            "group",
            "dream_outcome",
            "likelihood",
            "time_delay",
            "effort_sacrifice",
            "value_score",
        ]
    ],
    use_container_width=True,
)

# ---------- Outputs: chart ----------
st.markdown("#### 4. Visual comparison")

alt.themes.enable("none")

# Axis + title colours:
if theme_choice == "Dark":
    axis_label_color = "#393939"
    axis_title_color = "#393939"
    chart_title_color = "#393939"
else:
    axis_label_color = "#393939"
    axis_title_color = "#393939"
    chart_title_color = "#393939"

chart = (
    alt.Chart(df_scored)
    .mark_bar()
    .encode(
        x=alt.X("offer:N", sort="-y", title="Offer"),
        y=alt.Y("value_score:Q", title="Value score"),
        color=alt.Color(
            "group:N",
            title="Group",
            scale=alt.Scale(
                domain=["Company", "Competitor 1", "Competitor 2"],
                range=["#00E4AB", "#F2003C", "#fd7232"],
            ),
        ),
        tooltip=[
            alt.Tooltip("offer:N", title="Offer"),
            alt.Tooltip("group:N", title="Group"),
            alt.Tooltip("dream_outcome:Q", title="Dream outcome"),
            alt.Tooltip("likelihood:Q", title="Likelihood"),
            alt.Tooltip("time_delay:Q", title="Time delay"),
            alt.Tooltip("effort_sacrifice:Q", title="Effort & sacrifice"),
            alt.Tooltip("value_score:Q", title="Value score", format=".3f"),
        ],
    )
    .properties(
        height=380,
        title="Value score by offer",
    )
    .configure_title(
        color=chart_title_color,
        font="Inter",
        fontSize=16,
        anchor="start",
        fontWeight="bold",
    )
    .configure_view(stroke=None, fill="rgba(0,0,0,0)")
    .configure_axis(
        labelColor=axis_label_color,
        titleColor=axis_title_color,
        gridColor="rgba(148,163,184,0.25)",
        domainColor="rgba(148,163,184,0.55)",
    )
    .configure_legend(
        labelColor=axis_label_color,
        titleColor=axis_title_color,
        orient="top",
    )
)

st.altair_chart(chart, use_container_width=True)

# ---------- Download ----------
st.markdown("#### 5. Export results")
download_csv_button(df_scored)

# ---------- CSV helper ----------
with st.expander("CSV format example"):
    st.code(
        "offer,dream_outcome,likelihood,time_delay,effort_sacrifice,group\n"
        "Core Coaching,8,7,6,5,Company\n"
        "Premium Sprint,10,8,4,4,Company\n"
        "Competitor 1,9,7,5,6,Competitor 1",
        language="csv",
    )
