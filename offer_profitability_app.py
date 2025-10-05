import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

px.defaults.template = "plotly_dark"
st.set_page_config(page_title="Offer Profitability Analyzer", layout="wide")
st.title("Offer Profitability Analyzer — Expert Edition")

st.caption("Upload or edit offers data. Analyze revenue, gross profit, margins, Pareto, trends, and export results.")

sample = pd.DataFrame({
    "offer": ["Core Program","Premium Advisory","Workshop","Addon","Retainer"],
    "date": ["2025-01-15","2025-02-20","2025-01-05","2025-03-03","2025-04-01"],
    "segment": ["B2B","Enterprise","B2B","B2B","Enterprise"],
    "revenue": [150000, 240000, 20000, 30000, 96000],
    "cogs": [67500, 84000, 8000, 12000, 28800],
    "variable_costs": [15000, 30000, 3000, 4000, 12000],
    "units": [10, 6, 40, 20, 12]
})

with st.sidebar:
    st.header("Data")
    mode = st.radio("Mode", ["Upload CSV/XLSX", "Manual editor"], index=0)

if mode == "Upload CSV/XLSX":
    with st.sidebar:
        up = st.file_uploader("Upload file", type=["csv","xlsx"])
    if up is not None:
        if up.name.lower().endswith(".xlsx"):
            df = pd.read_excel(up)
        else:
            df = pd.read_csv(up)
    else:
        st.info("No file uploaded — using sample.")
        df = sample.copy()
else:
    if "df_edit" not in st.session_state:
        st.session_state.df_edit = sample.copy()
    df = st.data_editor(st.session_state.df_edit, num_rows="dynamic", use_container_width=True)
    st.session_state.df_edit = df.copy()
    st.download_button("⬇️ Download table (CSV)", data=df.to_csv(index=False), file_name="offers_current.csv", mime="text/csv")

st.markdown("---")
st.subheader("Column Mapping")
cols = list(df.columns)
def guess(names, default):
    for n in names:
        for c in cols:
            if c.lower().strip() == n:
                return c
    return default

offer_col = st.selectbox("Offer", cols, index=cols.index(guess(["offer","product","name"], cols[0])) if cols else 0)
rev_col   = st.selectbox("Revenue", cols, index=cols.index(guess(["revenue","sales","amount"], cols[0])) if cols else 0)
cogs_col  = st.selectbox("COGS", cols, index=cols.index(guess(["cogs","cost","cost_of_goods_sold"], cols[0])) if cols else 0)
date_col  = st.selectbox("Date (optional)", ["<none>"]+cols, index=(["<none>"]+cols).index(guess(["date","period"], "<none>")))
seg_col   = st.selectbox("Segment (optional)", ["<none>"]+cols, index=(["<none>"]+cols).index(guess(["segment","tier","channel"], "<none>")))
var_col   = st.selectbox("Variable costs (optional)", ["<none>"]+cols, index=(["<none>"]+cols).index(guess(["variable_costs","marketing_spend"], "<none>")))
units_col = st.selectbox("Units (optional)", ["<none>"]+cols, index=(["<none>"]+cols).index(guess(["units","qty","quantity"], "<none>")))

work = df.copy()
for c in [rev_col, cogs_col] + ([var_col] if var_col!="<none>" else []) + ([units_col] if units_col!="<none>" else []):
    if c!="<none>":
        work[c] = pd.to_numeric(work[c], errors="coerce")

if date_col!="<none>":
    work[date_col] = pd.to_datetime(work[date_col], errors="coerce")

mask = work[offer_col].notna() & work[rev_col].notna() & work[cogs_col].notna()
work = work[mask].copy()

work["gross_profit"] = work[rev_col] - work[cogs_col]
work["gross_margin_pct"] = np.where(work[rev_col]>0, work["gross_profit"]/work[rev_col], np.nan)
if var_col!="<none>":
    work["contribution_profit"] = work["gross_profit"] - work[var_col].fillna(0)
    work["contribution_margin_pct"] = np.where(work[rev_col]>0, work["contribution_profit"]/work[rev_col], np.nan)
if units_col!="<none>":
    work["revenue_per_unit"] = np.where(work[units_col]>0, work[rev_col]/work[units_col], np.nan)
    work["gross_profit_per_unit"] = np.where(work[units_col]>0, work["gross_profit"]/work[units_col], np.nan)

st.markdown("---")
st.subheader("Filters")
if seg_col!="<none>":
    segs = ["<All>"] + sorted(work[seg_col].dropna().unique().tolist())
    seg_pick = st.selectbox("Segment", segs, index=0)
else:
    seg_pick = "<All>"

if date_col!="<none>" and work[date_col].notna().any():
    min_d = work[date_col].min()
    max_d = work[date_col].max()
    rng = st.date_input("Date range", value=(min_d.date(), max_d.date()))
    if isinstance(rng, tuple) and len(rng)==2:
        start, end = pd.to_datetime(rng[0]), pd.to_datetime(rng[1])
        work = work[(work[date_col]>=start) & (work[date_col]<=end)]

if seg_pick!="<All>" and seg_col!="<none>":
    work = work[work[seg_col]==seg_pick]

st.markdown("---")
st.subheader("Offer Summary")
group_cols = [offer_col] + ([seg_col] if seg_col!="<none>" else [])
agg = {rev_col:"sum", cogs_col:"sum", "gross_profit":"sum"}
if var_col!="<none>":
    agg["contribution_profit"] = "sum"
if units_col!="<none>":
    agg[units_col] = "sum"
summ = work.groupby(group_cols).agg(agg).reset_index()
summ["gross_margin_pct"] = np.where(summ[rev_col]>0, summ["gross_profit"]/summ[rev_col], np.nan)
if "contribution_profit" in summ.columns:
    summ["contribution_margin_pct"] = np.where(summ[rev_col]>0, summ["contribution_profit"]/summ[rev_col], np.nan)

with st.sidebar:
    st.header("Sort by")
    metric = st.selectbox("Metric", [rev_col,"gross_profit","gross_margin_pct"] + (["contribution_profit","contribution_margin_pct"] if "contribution_profit" in summ.columns else []), index=1)
summ_sorted = summ.sort_values(metric, ascending=False)
st.dataframe(summ_sorted.round(3), use_container_width=True)

st.subheader("Charts")
top_n = st.slider("Top N (bar)", 3, 50, min(10, len(summ_sorted)), 1)
bar_df = summ.sort_values("gross_profit", ascending=False).head(top_n)
fig_bar = px.bar(bar_df, x=offer_col, y="gross_profit", color=rev_col, title="Top Offers by Gross Profit", hover_data=[rev_col, "gross_margin_pct"])
st.plotly_chart(fig_bar, use_container_width=True)
try:
    st.download_button("🖼️ Download bar (PNG)", data=fig_bar.to_image(format="png", scale=2), file_name="top_offers_gross_profit.png", mime="image/png")
except Exception:
    st.info("Install `kaleido` for PNG export.")

fig_sc = px.scatter(summ, x=rev_col, y="gross_margin_pct", text=offer_col, size="gross_profit", size_max=40, title="Revenue vs Gross Margin %")
fig_sc.update_traces(textposition="top center")
st.plotly_chart(fig_sc, use_container_width=True)
try:
    st.download_button("🖼️ Download scatter (PNG)", data=fig_sc.to_image(format="png", scale=2), file_name="revenue_vs_margin.png", mime="image/png")
except Exception:
    pass

st.subheader("Pareto (80/20)")
pareto = summ.sort_values(rev_col, ascending=False).reset_index(drop=True)
pareto["cum_revenue"] = pareto[rev_col].cumsum()
tot = pareto[rev_col].sum()
pareto["cum_share"] = np.where(tot>0, pareto["cum_revenue"]/tot, np.nan)
fig_p = px.line(pareto.reset_index(), x="index", y="cum_share", markers=True, title="Cumulative Revenue Share by Ranked Offer")
fig_p.add_hline(y=0.8, line_dash="dash", annotation_text="80% threshold", annotation_position="bottom right")
st.plotly_chart(fig_p, use_container_width=True)

if date_col!="<none>" and work[date_col].notna().any():
    st.subheader("Monthly Trends")
    ts = work.copy()
    ts["_month"] = ts[date_col].dt.to_period("M").dt.to_timestamp()
    ts_g = ts.groupby("_month").agg({rev_col:"sum","gross_profit":"sum"}).reset_index()
    ts_g["gross_margin_pct"] = np.where(ts_g[rev_col]>0, ts_g["gross_profit"]/ts_g[rev_col], np.nan)
    fig_ts = px.line(ts_g, x="_month", y=[rev_col,"gross_profit"], markers=True, title="Revenue & Gross Profit by Month")
    st.plotly_chart(fig_ts, use_container_width=True)
    try:
        st.download_button("🖼️ Download trends (PNG)", data=fig_ts.to_image(format="png", scale=2), file_name="monthly_trends.png", mime="image/png")
    except Exception:
        pass

st.markdown("---")
st.subheader("Quality Checks")
flags = []
if (work[rev_col] <= 0).any(): flags.append("Non-positive revenue rows detected.")
if (work["gross_profit"] < 0).any(): flags.append("Negative gross profit rows detected.")
if work["gross_margin_pct"].isna().any(): flags.append("Undefined margin % rows (likely revenue=0).")
st.write("- " + "\n- ".join(flags) if flags else "All checks passed.")

st.markdown("---")
st.subheader("Downloads")
st.download_button("⬇️ Offer summary (CSV)", data=summ_sorted.to_csv(index=False), file_name="offer_summary.csv", mime="text/csv")
st.download_button("⬇️ Pareto table (CSV)", data=pareto.to_csv(index=False), file_name="pareto_revenue.csv", mime="text/csv")
