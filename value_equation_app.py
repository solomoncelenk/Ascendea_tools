# -------------------------------
# Value Equation App (Streamlit)
# -------------------------------
# Ascendea Value Equation:
# Perceived Value = (Dream Outcome * Likelihood of Achievement) / (Time Delay * Effort & Sacrifice)
#
# CSV schema (headers, case-insensitive ok):
# offer, dream_outcome, likelihood, time_delay, effort_sacrifice [, group]
#
# Example row:
# "Premium Sprint", 10, 8, 4, 3, "Company"
#
# -------------------------------

import io
import math
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

# ---------- Page Config ----------
st.set_page_config(
    page_title="Value Equation Calculator",
    page_icon="📈",
    layout="wide"
)

# ---------- Helpers ----------
REQUIRED_COLS = ["offer", "dream_outcome", "likelihood", "time_delay", "effort_sacrifice"]
OPTIONAL_COLS = ["group"]  # e.g., "Company", "Competitor A", etc.

def canonicalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase + underscore column names; map common variants to required names."""
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
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    return missing

def compute_value_score(
    df: pd.DataFrame,
    w_outcome: float = 1.0,
    w_likelihood: float = 1.0,
    w_time: float = 1.0,
    w_effort: float = 1.0,
) -> pd.DataFrame:
    """
    Weighted Value Equation:
    ( (dream_outcome^w_outcome) * (likelihood^w_likelihood) )
    /
    ( (time_delay^w_time) * (effort_sacrifice^w_effort) )

    All factors expected on ~1-10 scale (lower is better for time/effort).
    """
    df = df.copy()
    # Avoid division by zero / invalids
    for col in ["dream_outcome", "likelihood", "time_delay", "effort_sacrifice"]:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)

    # Compute components with safety
    num = (df["dream_outcome"].clip(lower=1e-9) ** w_outcome) * (df["likelihood"].clip(lower=1e-9) ** w_likelihood)
    den = (df["time_delay"].clip(lower=1e-9) ** w_time) * (df["effort_sacrifice"].clip(lower=1e-9) ** w_effort)

    df["value_score"] = num / den
    return df

def starter_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "offer": ["Core Coaching", "Premium Sprint", "Enterprise Advisory"],
            "dream_outcome": [8, 10, 10],
            "likelihood": [7, 8, 9],
            "time_delay": [6, 4, 3],         # lower is better
            "effort_sacrifice": [5, 4, 3],   # lower is better
            "group": ["Company", "Company", "Company"],
        }
    )

def clean_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    df = canonicalize_columns(df)
    miss = validate_required_columns(df)
    if miss:
        raise ValueError(f"Missing required columns: {', '.join(miss)}")

    # Keep only recognized columns
    keep = [c for c in REQUIRED_COLS + OPTIONAL_COLS if c in df.columns]
    df = df[keep].copy()

    # Coerce numeric & bounds
    df = coerce_numeric(df, [c for c in REQUIRED_COLS if c != "offer"])
    # Clip to sensible ranges (1-10)
    for c in ["dream_outcome", "likelihood", "time_delay", "effort_sacrifice"]:
        df[c] = df[c].clip(lower=0.1, upper=10)

    # Fill group
    if "group" not in df.columns:
        df["group"] = "Company"

    # Clean offer names
    df["offer"] = df["offer"].astype(str).str.strip()
    return df

def download_csv_button(df: pd.DataFrame, filename: str = "value_equation_results.csv"):
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download results (CSV)", data=csv_bytes, file_name=filename, mime="text/csv")


# ---------- Sidebar ----------
st.sidebar.header("⚙️ Settings")
st.sidebar.write("Adjust factor weights (optional). 1.0 = neutral.")

w_outcome = st.sidebar.slider("Weight: Dream Outcome", 0.2, 3.0, 1.0, 0.1)
w_likelihood = st.sidebar.slider("Weight: Likelihood", 0.2, 3.0, 1.0, 0.1)
w_time = st.sidebar.slider("Weight: Time Delay (penalty)", 0.2, 3.0, 1.0, 0.1)
w_effort = st.sidebar.slider("Weight: Effort & Sacrifice (penalty)", 0.2, 3.0, 1.0, 0.1)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Tip: Lower **Time Delay** and **Effort** scores indicate less friction. "
    "If your data uses the opposite meaning, normalize before upload."
)

# ---------- Header ----------
st.title("📈 Value Equation Calculator")
st.write(
    "Compute perceived value for each offer using Hormozi’s Value Equation. "
    "Upload a CSV or use the inline editor, then compare offers and export results."
)

# ---------- Data Ingest ----------
uploaded = st.file_uploader("Upload CSV (offer, dream_outcome, likelihood, time_delay, effort_sacrifice, [group])", type=["csv"])

if uploaded is not None:
    try:
        raw = pd.read_csv(uploaded)
        df_in = clean_and_prepare(raw)
        st.success("CSV loaded successfully.")
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()
else:
    st.info("No CSV uploaded. Use the editable table below to get started.")
    df_in = starter_dataframe()

st.markdown("### ✍️ Edit / Review Data")
edited = st.data_editor(
    df_in,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "offer": st.column_config.TextColumn("Offer", help="Name of the offer/product/package"),
        "dream_outcome": st.column_config.NumberColumn("Dream Outcome (1-10)"),
        "likelihood": st.column_config.NumberColumn("Likelihood (1-10)"),
        "time_delay": st.column_config.NumberColumn("Time Delay (1-10, lower=better)"),
        "effort_sacrifice": st.column_config.NumberColumn("Effort & Sacrifice (1-10, lower=better)"),
        "group": st.column_config.TextColumn("Group (optional)"),
    }
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

# Rank
df_scored["rank"] = df_scored["value_score"].rank(ascending=False, method="dense").astype(int)
df_scored = df_scored.sort_values(["rank", "value_score"], ascending=[True, False]).reset_index(drop=True)

# ---------- Outputs ----------
st.markdown("### 🧮 Results (Ranked)")
st.dataframe(
    df_scored[["rank", "offer", "group", "dream_outcome", "likelihood", "time_delay", "effort_sacrifice", "value_score"]],
    use_container_width=True
)

# Chart
st.markdown("### 📊 Value Score by Offer")
chart = (
    alt.Chart(df_scored)
    .mark_bar()
    .encode(
        x=alt.X("offer:N", sort="-y", title="Offer"),
        y=alt.Y("value_score:Q", title="Value Score"),
        color=alt.Color("group:N", title="Group"),
        tooltip=[
            alt.Tooltip("offer:N"),
            alt.Tooltip("group:N"),
            alt.Tooltip("dream_outcome:Q"),
            alt.Tooltip("likelihood:Q"),
            alt.Tooltip("time_delay:Q"),
            alt.Tooltip("effort_sacrifice:Q"),
            alt.Tooltip("value_score:Q", format=".3f"),
        ],
    )
    .properties(height=380)
)
st.altair_chart(chart, use_container_width=True)

# Download
st.markdown("### ⬇️ Export")
download_csv_button(df_scored)

# ---------- Guidance ----------
with st.expander("How this works"):
    st.write(
        """
        **Value Equation** = (Dream Outcome × Likelihood of Achievement) ÷ (Time Delay × Effort & Sacrifice).

        - Increase value by **raising** Dream Outcome and Likelihood.
        - Increase value by **lowering** Time Delay and Effort & Sacrifice.
        - Use the sliders in the sidebar to apply **weights** if certain factors matter more in your market.
        """
    )

with st.expander("CSV format example"):
    st.code(
        "offer,dream_outcome,likelihood,time_delay,effort_sacrifice,group\n"
        "Core Coaching,8,7,6,5,Company\n"
        "Premium Sprint,10,8,4,4,Company\n"
        "Competitor A,9,7,5,6,Competitor",
        language="csv",
    )

