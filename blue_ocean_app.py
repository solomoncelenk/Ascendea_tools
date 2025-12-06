# Blue Ocean Strategy Canvas – Ascendea UI (with numeric editor)

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------- Page config ----------
st.set_page_config(page_title="Ascendea – Blue Ocean Strategy Canvas", layout="wide")

# ---------- Theme tokens ----------
DARK_TOKENS = {
    "PRIMARY": "#ffffff",
    "MUTED": "rgba(255,255,255,0.78)",
    "DISABLED": "rgba(255,255,255,0.45)",
    "BG": "#050814",
}

LIGHT_TOKENS = {
    "PRIMARY": "#0b1020",
    "MUTED": "#4b5563",
    "DISABLED": "#9ca3af",
    "BG": "#f5f7fb",
}

# ---------- Sidebar: theme + data mode ----------
with st.sidebar:
    st.header("Display & Data")

    theme_choice = st.radio("Theme", ["Dark", "Light"], index=0, horizontal=True)
    TOKENS = DARK_TOKENS if theme_choice == "Dark" else LIGHT_TOKENS

    st.markdown("---")
    st.header("Data source")

    mode = st.radio("Choose data mode", ["Manual editor", "Upload CSV"], index=0)
    st.caption("CSV must be wide format with columns: value_factor, Our Offer, Competitor 1, Competitor 2, ...")

# ---------- Global CSS ----------
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
  max-width: 780px;
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

/* Buttons */
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
  max-width: 780px;
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

/* Buttons */
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

# ---------- Sample data ----------
sample_df = pd.DataFrame({
    "value_factor": ["Price","Speed","Customization","Support","Brand","Risk Reduction"],
    "Our Offer":   [6, 8, 7, 9, 8, 7],
    "Competitor 1":[8, 6, 5, 7, 7, 6],
    "Competitor 2":[7, 7, 6, 6, 9, 5]
})

# ---------- Header + how it works ----------
st.markdown(
    """
    <div class="asc-card">
      <div class="asc-eyebrow">Ascendea Strategy Architecture</div>
      <div class="asc-title">Blue Ocean Strategy Canvas</div>
      <div class="asc-subtitle">
        Compare buyer value factors across competitors, visualise your strategy canvas,
        and translate the gaps into Eliminate / Reduce / Raise / Create moves.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="asc-card">
      <div class="asc-eyebrow">How this canvas works</div>
      <div class="asc-subtitle" style="margin-top:0.5rem;">
        1. Choose the <strong>buyer value factors</strong> that actually drive decisions in your market.<br/>
        2. Score your offer and each competitor from 0–10 on every factor.<br/>
        3. Read the <strong>strategy canvas</strong> lines to see where you're overinvesting, underinvesting, or matching the herd.<br/>
        4. Use the ERRC grid to decide what to <strong>Eliminate, Reduce, Raise, Create</strong> in your offer and go-to-market.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Data mode handling ----------
if mode == "Upload CSV":
    with st.sidebar:
        uploaded = st.file_uploader("Upload strategy_canvas_data.csv", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        st.info("No file uploaded — using sample data.")
        df = sample_df.copy()
else:
    if "bo_df" not in st.session_state:
        st.session_state.bo_df = sample_df.copy()
    if "our_label" not in st.session_state:
        st.session_state.our_label = "Our Offer"

    with st.sidebar:
        st.subheader("Our label & competitors")
        our_label = st.text_input("Rename 'Our Offer' label", value=st.session_state.our_label)
        if our_label != st.session_state.our_label and st.session_state.our_label in st.session_state.bo_df.columns:
            st.session_state.bo_df = st.session_state.bo_df.rename(columns={st.session_state.our_label: our_label})
            st.session_state.our_label = our_label

        new_comp = st.text_input("Add competitor (press Enter)")
        if new_comp and new_comp not in st.session_state.bo_df.columns and new_comp != st.session_state.our_label:
            st.session_state.bo_df[new_comp] = 5
            st.success(f"Added column: {new_comp}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Reset to sample"):
                st.session_state.bo_df = sample_df.copy()
                st.session_state.our_label = "Our Offer"
        with c2:
            st.download_button(
                "⬇️ Download current table (CSV)",
                data=st.session_state.bo_df.to_csv(index=False),
                file_name="strategy_canvas_data.csv",
                mime="text/csv",
            )

    # ---------- Numeric-aware editor ----------
    col_config = {
        "value_factor": st.column_config.TextColumn(
            "value_factor",
            help="Buyer value factor (e.g. Price, Speed, Support).",
        )
    }
    for c in st.session_state.bo_df.columns:
        if c != "value_factor":
            col_config[c] = st.column_config.NumberColumn(
                c,
                help=f"Score for {c} (0–10).",
                min_value=0,
                max_value=10,
                step=1,
                format="%d",
            )

    df = st.data_editor(
        st.session_state.bo_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config=col_config,
    )
    st.session_state.bo_df = df.copy()

# ---------- Validate & clean ----------
if "value_factor" not in df.columns:
    st.error("Your data needs a 'value_factor' column.")
    st.stop()

series_cols = [c for c in df.columns if c != "value_factor"]
if len(series_cols) < 2:
    st.error("Add at least two series columns (e.g., 'Our Offer' and one competitor).")
    st.stop()

for col in series_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=series_cols, how="all")
if df.empty:
    st.error("No valid numeric scores found.")
    st.stop()

for col in series_cols:
    df[col] = df[col].clip(0, 10)

our_guess = next((c for c in series_cols if "our" in c.lower()), series_cols[0])
with st.sidebar:
    our_label_select = st.selectbox(
        "Select your series (Our Offer):",
        series_cols,
        index=series_cols.index(our_guess) if our_guess in series_cols else 0,
    )

# ---------- Strategy canvas chart ----------
st.subheader("Strategy Canvas")

long = df.melt(id_vars="value_factor", var_name="Series", value_name="Score")

# Branded colour mapping: Our Offer = teal, Competitor 1 = red, Competitor 2 = orange
base_colors = {
    "Our Offer": "#00E4AB",
    "Competitor 1": "#F2003C",
    "Competitor 2": "#fd7232",
}

# Build colour map for plotly based on series order
color_discrete_map = {}
palette_fallback = ["#7b61ff", "#f5b700", "#10b981", "#6366f1", "#ec4899"]
fallback_index = 0
for s in long["Series"].unique():
    if s in base_colors:
        color_discrete_map[s] = base_colors[s]
    else:
        if fallback_index < len(palette_fallback):
            color_discrete_map[s] = palette_fallback[fallback_index]
            fallback_index += 1
        else:
            color_discrete_map[s] = "#999999"

fig = px.line(
    long,
    x="value_factor",
    y="Score",
    color="Series",
    markers=True,
    title="Strategy Canvas — Buyer Value Factors (0–10)",
    color_discrete_map=color_discrete_map,
)

# Axis + title colours
axis_color = "#ffffff" if theme_choice == "Dark" else "#393939"

fig.update_layout(
    xaxis_title="Buyer value factors",
    yaxis_title="Performance (0–10)",
    yaxis=dict(range=[0, 10]),
    legend_title="Series",
    title_font=dict(family="Inter", size=16, color=axis_color),
    font=dict(family="Inter", color=axis_color),
)
fig.update_xaxes(showgrid=True, gridcolor="rgba(148,163,184,0.25)", linecolor="rgba(148,163,184,0.55)")
fig.update_yaxes(showgrid=True, gridcolor="rgba(148,163,184,0.25)", linecolor="rgba(148,163,184,0.55)")

st.plotly_chart(fig, use_container_width=True)

# ---------- ERRC Grid ----------
st.markdown("---")
st.subheader("ERRC Grid (Eliminate · Reduce · Raise · Create)")

competitor_cols = [c for c in series_cols if c != our_label_select]
if competitor_cols:
    comp_mean = df[competitor_cols].mean(axis=1)
else:
    comp_mean = pd.Series([np.nan] * len(df), index=df.index)

gap = df[our_label_select] - comp_mean
suggest = []
for i, row in df.iterrows():
    factor = row["value_factor"]
    g = gap.loc[i] if not np.isnan(gap.loc[i]) else 0
    if g <= -1.0:
        action = "Raise"
        rationale = "We underperform vs competitors here; raising this factor could unlock parity or differentiation."
    elif g >= 1.0:
        action = "Reduce"
        rationale = "We overinvest vs competitors; consider reducing emphasis if not critical to ICP priorities."
    else:
        action = "Keep"
        rationale = "Similar to competitors; keep as is unless ICP research says otherwise."
    suggest.append(
        {
            "value_factor": factor,
            "action": action,
            "rationale": rationale,
            "gap_vs_comp": round(float(g), 2),
        }
    )

errc_df = pd.DataFrame(suggest)
st.info("Tip: Change 'action' per factor or add new rows for CREATE (new value factors).")
errc_editable = st.data_editor(
    errc_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "action": st.column_config.SelectboxColumn(
            "action",
            options=["Eliminate", "Reduce", "Raise", "Create", "Keep"],
        )
    },
)

# ---------- Offer differentiation report ----------
st.markdown("---")
st.subheader("Offer Differentiation Report")

df_tmp = df.copy()
df_tmp["comp_mean"] = comp_mean
df_tmp["gap_vs_comp"] = df_tmp[our_label_select] - df_tmp["comp_mean"]
under = df_tmp.nsmallest(3, "gap_vs_comp")[["value_factor", "gap_vs_comp"]]
over = df_tmp.nlargest(3, "gap_vs_comp")[["value_factor", "gap_vs_comp"]]

lines = []
lines.append(f"**Our series:** {our_label_select}")
lines.append("")
lines.append("**Where we trail competitors (priority to Raise):**")
for _, r in under.iterrows():
    lines.append(f"- {r['value_factor']}: gap {r['gap_vs_comp']:.2f}")
lines.append("")
lines.append("**Where we lead competitors (candidates to Reduce/Exploit):**")
for _, r in over.iterrows():
    lines.append(f"- {r['value_factor']}: gap +{r['gap_vs_comp']:.2f}")
lines.append("")
act_counts = errc_editable["action"].value_counts().to_dict() if not errc_editable.empty else {}
summary_bits = [f"{k}={v}" for k, v in act_counts.items()]
lines.append("**ERRC Summary:** " + (", ".join(summary_bits) if summary_bits else "No actions selected yet."))
lines.append("")
lines.append(
    "**Next moves:** Translate the ERRC selections into concrete changes (pricing, features, delivery, proof, messaging) mapped to ICP priorities."
)

report_md = "\n".join(lines)
st.markdown(report_md)

st.download_button(
    "⬇️ Download report (Markdown)",
    data=report_md,
    file_name="offer_differentiation_report.md",
    mime="text/markdown",
)
st.download_button(
    "⬇️ Download ERRC grid (CSV)",
    data=errc_editable.to_csv(index=False),
    file_name="errc_grid.csv",
    mime="text/csv",
)
