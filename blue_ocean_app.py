import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

px.defaults.template = "plotly_dark"

st.set_page_config(page_title="Blue Ocean Strategy Canvas", layout="wide")
st.title("Blue Ocean Strategy Canvas — Strategy & ERRC")

st.caption("Compare buyer value factors across competitors, visualise your strategy canvas, and turn insights into Eliminate/Reduce/Raise/Create moves.")

sample_df = pd.DataFrame({
    "value_factor": ["Price","Speed","Customization","Support","Brand","Risk Reduction"],
    "Our Offer":   [6, 8, 7, 9, 8, 7],
    "Competitor A":[8, 6, 5, 7, 7, 6],
    "Competitor B":[7, 7, 6, 6, 9, 5]
})

with st.sidebar:
    st.header("Data")
    mode = st.radio("Choose data mode", ["Manual editor", "Upload CSV"], index=0)
    st.caption("CSV must be wide format with columns: value_factor, Our Offer, Competitor A, ...")

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
        if c1.button("Reset to sample"):
            st.session_state.bo_df = sample_df.copy()
            st.session_state.our_label = "Our Offer"
        st.download_button("⬇️ Download current table (CSV)",
                           data=st.session_state.bo_df.to_csv(index=False),
                           file_name="strategy_canvas_data.csv",
                           mime="text/csv")

    df = st.data_editor(
        st.session_state.bo_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "value_factor": st.column_config.TextColumn("value_factor"),
        }
    )
    st.session_state.bo_df = df.copy()

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
    our_label_select = st.selectbox("Select your series (Our Offer):", series_cols, index=series_cols.index(our_guess) if our_guess in series_cols else 0)

st.subheader("Strategy Canvas")
long = df.melt(id_vars="value_factor", var_name="Series", value_name="Score")

fig = px.line(long, x="value_factor", y="Score", color="Series", markers=True,
              title="Strategy Canvas — Buyer Value Factors (1–10)")
fig.update_layout(xaxis_title="Buyer Values", yaxis_title="Performance (1–10)",
                  yaxis=dict(range=[0,10]), legend_title="Series")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("ERRC Grid (Eliminate · Reduce · Raise · Create)")

competitor_cols = [c for c in series_cols if c != our_label_select]
if competitor_cols:
    comp_mean = df[competitor_cols].mean(axis=1)
else:
    comp_mean = pd.Series([np.nan]*len(df), index=df.index)

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
    suggest.append({"value_factor": factor, "action": action, "rationale": rationale, "gap_vs_comp": round(float(g), 2)})

errc_df = pd.DataFrame(suggest)
st.info("Tip: Change 'action' per factor or add new rows for CREATE (new value factors).")
errc_editable = st.data_editor(
    errc_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "action": st.column_config.SelectboxColumn("action", options=["Eliminate","Reduce","Raise","Create","Keep"])
    }
)

st.markdown("---")
st.subheader("Offer Differentiation Report")

df_tmp = df.copy()
df_tmp["comp_mean"] = comp_mean
df_tmp["gap_vs_comp"] = df_tmp[our_label_select] - df_tmp["comp_mean"]
under = df_tmp.nsmallest(3, "gap_vs_comp")[["value_factor","gap_vs_comp"]]
over  = df_tmp.nlargest(3,  "gap_vs_comp")[["value_factor","gap_vs_comp"]]

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
summary_bits = [f"{k}={v}" for k,v in act_counts.items()]
lines.append("**ERRC Summary:** " + (", ".join(summary_bits) if summary_bits else "No actions selected yet."))
lines.append("")
lines.append("**Next moves:** Translate the ERRC selections into concrete changes (pricing, features, delivery, proof, messaging) mapped to ICP priorities.")

report_md = "\n".join(lines)
st.markdown(report_md)

st.download_button("⬇️ Download report (Markdown)", data=report_md, file_name="offer_differentiation_report.md", mime="text/markdown")
st.download_button("⬇️ Download ERRC grid (CSV)",
                   data=errc_editable.to_csv(index=False),
                   file_name="errc_grid.csv",
                   mime="text/csv")
