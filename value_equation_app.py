import streamlit as st
import pandas as pd
import plotly.express as px

px.defaults.template = "plotly_dark"

st.set_page_config(page_title="Value Equation Scorecard", layout="wide")
st.title("Hormozi Value Equation — Offer Scorecard")

with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload value_equation_template.csv", type=["csv"])
    st.caption("Columns required: offer, brand, dream_outcome, likelihood, time_delay, effort_sacrifice (1–10 scales)")

if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    st.info("No file uploaded — using sample data.")
    df = pd.DataFrame({
        "offer": ["Core Coaching","Premium Sprint","Enterprise Advisory","Competitor A","Competitor B"],
        "brand": ["Us","Us","Us","Competitor","Competitor"],
        "dream_outcome": [9,10,10,8,9],
        "likelihood": [7,8,9,6,7],
        "time_delay": [6,4,3,7,6],
        "effort_sacrifice": [5,4,3,6,6]
    })

required = {"offer","brand","dream_outcome","likelihood","time_delay","effort_sacrifice"}
missing = required - set(df.columns)
if missing:
    st.error(f"Missing columns: {', '.join(sorted(missing))}")
    st.stop()

for c in ["dream_outcome","likelihood","time_delay","effort_sacrifice"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
if df[["dream_outcome","likelihood","time_delay","effort_sacrifice"]].isna().any().any():
    st.error("Some numeric fields could not be parsed. Check your CSV.")
    st.stop()

with st.sidebar:
    st.header("Weights Profile")
    profile = st.selectbox("Preset Profiles", ["Default","Enterprise Buyer","SMB Buyer","Transformation Buyer"])

    if profile == "Enterprise Buyer":
        w_do, w_l, w_t, w_e = 1.0, 1.5, 1.0, 0.8
    elif profile == "SMB Buyer":
        w_do, w_l, w_t, w_e = 1.0, 1.0, 1.5, 1.0
    elif profile == "Transformation Buyer":
        w_do, w_l, w_t, w_e = 1.5, 1.0, 1.0, 1.0
    else:
        w_do, w_l, w_t, w_e = 1.0, 1.0, 1.0, 1.0

    w_do = st.slider("Dream Outcome weight", 0.1, 3.0, w_do, 0.1)
    w_l  = st.slider("Likelihood weight", 0.1, 3.0, w_l, 0.1)
    w_t  = st.slider("Time Delay weight", 0.1, 3.0, w_t, 0.1)
    w_e  = st.slider("Effort & Sacrifice weight", 0.1, 3.0, w_e, 0.1)

df["value_score"] = ((df["dream_outcome"]**w_do) * (df["likelihood"]**w_l)) /                     ((df["time_delay"]**w_t) * (df["effort_sacrifice"]**w_e))
df["value_index_100"] = 100 * (df["value_score"] / df["value_score"].max())

left, right = st.columns([1.1, 1])
with left:
    st.subheader("Scorecard")
    show_cols = ["offer","brand","dream_outcome","likelihood","time_delay","effort_sacrifice","value_score","value_index_100"]
    st.dataframe(df[show_cols].sort_values("value_score", ascending=False).round(3), use_container_width=True)

with right:
    st.subheader("Comparison")
    fig = px.bar(df.sort_values("value_score", ascending=False),
                 x="offer", y="value_score", color="brand", title="Value Score by Offer")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Radar Comparison (Offer Diagnostics)")
melted = df.melt(id_vars=["offer","brand"],
                 value_vars=["dream_outcome","likelihood","time_delay","effort_sacrifice"],
                 var_name="Dimension", value_name="Score")
fig_radar = px.line_polar(melted, r="Score", theta="Dimension", color="offer", line_close=True,
                          title="Offer Profiles (1–10 scale)")
fig_radar.update_traces(fill='toself', opacity=0.6)
st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")
st.subheader("Diagnostics & Recommendations")

def rec_row(row):
    tips = []
    if row["time_delay"] >= 6:
        tips.append("Reduce time-to-result with faster onboarding, prebuilt assets, or parallel workstreams.")
    if row["effort_sacrifice"] >= 6:
        tips.append("Lower client lift: done-for-you components, templates, concierge setup, or clearer expectations.")
    if row["likelihood"] <= 7:
        tips.append("Raise proof: stronger case studies, quantified outcomes, guarantees, success metrics, social proof density.")
    if row["dream_outcome"] <= 8:
        tips.append("Increase perceived outcome: sharpen promise, tie to $$ impact, add compelling before/after states.")
    return " • ".join(tips) or "Strong fit; focus on durable proof and speed."

diag = df.copy()
diag["recommendations"] = diag.apply(rec_row, axis=1)
st.dataframe(diag[["offer","brand","value_score","recommendations"]].sort_values("value_score", ascending=False),
             use_container_width=True)

csv = df.sort_values("value_score", ascending=False).to_csv(index=False)
st.download_button("⬇️ Download scored offers (CSV)", data=csv, file_name="value_equation_scored.csv", mime="text/csv")

st.caption("Equation: (Dream Outcome × Likelihood) / (Time Delay × Effort & Sacrifice). Lower Time/Effort increase value.")
