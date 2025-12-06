# -------------------------------
# Value Equation App (Streamlit) – Ascendea UI
# -------------------------------
# Ascendea Value Equation:
# Perceived Value = (Dream Outcome * Likelihood of Achievement) / (Time Delay * Effort & Sacrifice)
#
# CSV schema (headers, case-insensitive ok):
# offer, dream_outcome, likelihood, time_delay, effort_sacrifice [, group]
# -------------------------------

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

# ---------- Brand Tokens ----------
ASC_TEAL = "#4ebfb0"
ASC_RED = "#ee4128"
ASC_BG = "#050814"
ASC_WHITE = "#ffffff"
ASC_MUTED = "rgba(255,255,255,0.75)"

# ---------- Page Config ----------
st.set_page_config(
    page_title="Ascendea – Value Equation Calculator",
    page_icon="📈",
    layout="wide",
)

# ---------- Global CSS (Ascendea shell + mobile tweaks) ----------
CUSTOM_CSS = """
<style>
/* Load Inter */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="stApp"] {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
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

/* Sidebar styling */
section[data-testid="stSidebar"] {
  background: linear-gradient(160deg, #050814 0%, #090f1f 40%, #141a32 100%);
  border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] .sidebar-content {
  padding-top: 1.5rem;
}

/* Card shells */
.asc-card {
  border-radius: 24px;
  border: 1px solid rgba(255,255,255,0.12);
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

/* Section headers */
.asc-eyebrow {
  font-size: 0.78rem;
  letter-spacing: 0.26em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.78);
}

.asc-title {
  font-size: 1.9rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-top: 0.35rem;
  margin-bottom: 0.4rem;
}

.asc-title span {
  color: #4ebfb0;
}

.asc-subtitle {
  font-size: 0.98rem;
  color: rgba(255,255,255,0.75);
  max-width: 720px;
}

/* Data table tweaks */
.dataframe tbody tr th {
  color: #ffffff;
}

.dataframe thead th {
  background: rgba(11,16,35,0.9);
}

.dataframe tbody tr:nth-child(even) {
  background: rgba(6,9,24,0.85);
}

.dataframe tbody tr:nth-child(odd) {
  background: rgba(9,13,28,0.95);
}

.dataframe td, .dataframe th {
  border-color: rgba(255,255,255,0.06) !important;
}

/* Download button alignment */
.asc-download-wrap {
  margin-top: 0.75rem;
}

/* Mobile adjustments */
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

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------- Helpers ----------
REQUIRED_COLS = ["offer", "dream_outcome", "likelihood", "time_delay", "effort_sacrifice"]
OPTIONAL_COLS = ["group"]  # e.g., "Company", "Competitor A", etc.


def canonicalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase + underscore column names; map common variants to required names."""
    mapping = {
        "offer": "offer",
