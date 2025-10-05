import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

px.defaults.template = "plotly_dark"

st.set_page_config(page_title="Offer Ecosystem Map", layout="wide")
st.title("Offer Ecosystem Map — Tiers, Flows, Finance & Strategy")

st.caption("Visualise Entry → Core → Premium → Upsell → Recurring, layer Blue Ocean & Psychology, and run financial diagnostics.")

TIERS = ["Entry","Core","Premium","Upsell","Recurring"]

sample_offers = pd.DataFrame({
    "offer": ["Free Workshop","Core Program","Premium Advisory","Cross-sell Addon","Growth Retainer"],
    "tier": ["Entry","Core","Premium","Upsell","Recurring"],
    "price": [0, 15000, 60000, 5000, 0],
    "mrr": [0, 0, 0, 0, 8000],
    "term_months": [0, 0, 0, 0, 12],
    "margin_pct": [0.20, 0.55, 0.65, 0.60, 0.70],
    "anchor": [False, False, True, False, False],
    "scarcity": [False, False, True, True, False],
    "positioning_frame": ["Workshop","Program","Partnership","Add-on","Retainer"],
    "enabled": [True, True, True, True, True],
    "notes": ["Lead magnet","Flagship delivery","Exec-only tier","Sold post-core","Monthly subscription"]
})

sample_flows = pd.DataFrame({
    "source_tier": ["Entry","Core","Core","Premium","Core","Premium","Entry"],
    "target_tier": ["Core","Premium","Upsell","Recurring","Recurring","Recurring","Core"],
    "label": ["Low-friction lead in","Advance","Upsell","Anchor","Anchor","Anchor","Feeds"],
    "prob": [0.30, 0.35, 0.25, 0.70, 0.50, 0.80, 0.30],
    "notes": ["Entry→Core conversion","Core→Premium","Cross-sell rate","Premium to Retainer","Core to Retainer","Premium to Retainer","Entry→Core repeat"]
})

sample_errc = pd.DataFrame({
    "offer": ["Free Workshop","Core Program","Premium Advisory","Cross-sell Addon","Growth Retainer"],
    "action": ["Create","Raise","Create","Reduce","Raise"],
    "rationale": ["Add more pain-specific themes","Strengthen proof & speed","Anchor Core via exec layer","Bundle to increase take rate","Make retainer default post-core"]
})

with st.sidebar:
    st.header("Data")
    mode = st.radio("Choose data mode", ["Manual editor", "Upload CSVs"], index=0)
    st.caption("Upload `offers.csv`, `flows.csv`, (optional) `errc.csv`.")

def read_or_default(uploaded_list):
    frames = {"offers": None, "flows": None, "errc": None}
    sigs = {
        "offers": {"offer","tier","price","mrr","term_months","margin_pct","anchor","scarcity","positioning_frame","enabled","notes"},
        "flows": {"source_tier","target_tier","label","prob","notes"},
        "errc": {"offer","action","rationale"}
    }
    if uploaded_list:
        for f in uploaded_list:
            try:
                df = pd.read_csv(f)
            except Exception:
                continue
            name = (f.name or "").lower()
            matched = None
            for key, sig in sigs.items():
                if sig.issubset(set(df.columns)) or key in name:
                    frames[key] = df
                    matched = key
                    break
            if not matched and set(df.columns) == sigs["offers"]:
                frames["offers"] = df
    frames["offers"] = frames["offers"] or sample_offers.copy()
    frames["flows"]  = frames["flows"]  or sample_flows.copy()
    frames["errc"]   = frames["errc"]   or sample_errc.copy()
    return frames

if mode == "Upload CSVs":
    with st.sidebar:
        uploads = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)
    frames = read_or_default(uploads)
else:
    if "eco_frames" not in st.session_state:
        st.session_state.eco_frames = {"offers": sample_offers.copy(),
                                       "flows": sample_flows.copy(),
                                       "errc": sample_errc.copy()}
    with st.sidebar:
        c1, c2 = st.columns(2)
        if c1.button("Reset to sample"):
            st.session_state.eco_frames = {"offers": sample_offers.copy(),
                                           "flows": sample_flows.copy(),
                                           "errc": sample_errc.copy()}
        st.download_button("⬇️ Download offers.csv", st.session_state.eco_frames["offers"].to_csv(index=False), "offers.csv", "text/csv")
        st.download_button("⬇️ Download flows.csv",  st.session_state.eco_frames["flows"].to_csv(index=False),  "flows.csv",  "text/csv")
        st.download_button("⬇️ Download errc.csv",   st.session_state.eco_frames["errc"].to_csv(index=False),   "errc.csv",   "text/csv")

    st.subheader("Offers (tiers & economics)")
    st.caption("Columns: tier (Entry/Core/Premium/Upsell/Recurring), price (one-time), mrr (monthly), term_months (recurring), margin_pct (0–1)")
    st.session_state.eco_frames["offers"] = st.data_editor(
        st.session_state.eco_frames["offers"],
        num_rows="dynamic", use_container_width=True,
        column_config={
            "tier": st.column_config.SelectboxColumn("tier", options=TIERS),
            "margin_pct": st.column_config.NumberColumn("margin_pct", min_value=0.0, max_value=1.0, step=0.05),
            "enabled": st.column_config.CheckboxColumn("enabled", default=True),
            "anchor": st.column_config.CheckboxColumn("anchor", default=False),
            "scarcity": st.column_config.CheckboxColumn("scarcity", default=False),
        }
    )

    st.subheader("Flows (tier-level)")
    st.caption("Probabilities (0–1) define % moving from source → target per period/cohort.")
    st.session_state.eco_frames["flows"] = st.data_editor(
        st.session_state.eco_frames["flows"],
        num_rows="dynamic", use_container_width=True,
        column_config={
            "source_tier": st.column_config.SelectboxColumn("source_tier", options=TIERS),
            "target_tier": st.column_config.SelectboxColumn("target_tier", options=TIERS),
            "prob": st.column_config.NumberColumn("prob", min_value=0.0, max_value=1.0, step=0.05)
        }
    )

    st.subheader("ERRC grid (offer-level)")
    st.session_state.eco_frames["errc"] = st.data_editor(
        st.session_state.eco_frames["errc"],
        num_rows="dynamic", use_container_width=True,
        column_config={
            "action": st.column_config.SelectboxColumn("action", options=["Eliminate","Reduce","Raise","Create","Keep"])
        }
    )

    frames = st.session_state.eco_frames

offers = frames["offers"].copy()
flows  = frames["flows"].copy()
errc   = frames["errc"].copy()

with st.sidebar:
    st.header("Assumptions")
    cohort = st.number_input("Entry cohort size (customers)", min_value=0, value=1000, step=50)
    months = st.number_input("Recurring term for MRR (months)", min_value=1, value=12, step=1)

offers["enabled"] = offers["enabled"].astype(bool)
offers = offers[offers["enabled"]]
offers["tier"] = offers["tier"].astype(str)

for c in ["price","mrr","term_months","margin_pct"]:
    offers[c] = pd.to_numeric(offers[c], errors="coerce").fillna(0.0)

flows["prob"] = pd.to_numeric(flows["prob"], errors="coerce").fillna(0.0)
flows = flows[flows["source_tier"].isin(TIERS) & flows["target_tier"].isin(TIERS)]

tier_fin = offers.groupby("tier").agg(
    avg_price=("price","mean"),
    avg_mrr=("mrr","mean"),
    avg_term=("term_months","mean"),
    avg_margin=("margin_pct","mean"),
    n_offers=("offer","count")
).reindex(TIERS).fillna(0.0).reset_index()

cust = {t: 0.0 for t in TIERS}
cust["Entry"] = float(cohort)

flow_matrix = flows.groupby(["source_tier","target_tier"])["prob"].sum().clip(upper=1.0).reset_index()

order = ["Entry","Core","Premium","Upsell","Recurring"]
for src in order:
    base = cust[src]
    if base <= 0:
        continue
    outgoing = flow_matrix[flow_matrix["source_tier"]==src]
    for _, row in outgoing.iterrows():
        tgt = row["target_tier"]
        cust[tgt] += base * row["prob"]

rev = {}
rev_margin = {}
for _, row in tier_fin.iterrows():
    tier = row["tier"]
    customers = cust.get(tier, 0.0)
    one_time_revenue = customers * row["avg_price"]
    recurring_revenue = customers * row["avg_mrr"] * (months if tier!="Recurring" else row["avg_term"] if row["avg_term"]>0 else months)
    total_rev = one_time_revenue + recurring_revenue
    rev[tier] = total_rev
    rev_margin[tier] = total_rev * row["avg_margin"]

rev_df = pd.DataFrame({
    "tier": TIERS,
    "expected_customers": [cust[t] for t in TIERS],
    "revenue": [rev[t] for t in TIERS],
    "contribution": [rev_margin[t] for t in TIERS],
    "avg_margin_pct": [tier_fin[tier_fin['tier']==t]["avg_margin"].values[0] if t in tier_fin["tier"].values else 0 for t in TIERS]
})

st.markdown("---")
st.subheader("Flow Map (Sankey)")

links = flows.copy()
links = links.merge(pd.DataFrame({"tier": list(cust.keys()), "expected_customers": list(cust.values())}),
                    left_on="source_tier", right_on="tier", how="left")
links["value"] = (links["prob"] * links["expected_customers"]).round(2)
labels = TIERS
lab_to_idx = {lab:i for i,lab in enumerate(labels)}
source_idx = links["source_tier"].map(lab_to_idx).tolist()
target_idx = links["target_tier"].map(lab_to_idx).tolist()
values = links["value"].tolist()

sankey_fig = go.Figure(data=[go.Sankey(
    arrangement="snap",
    node=dict(label=labels, pad=20, thickness=18),
    link=dict(source=source_idx, target=target_idx, value=values, label=links["label"])
)])
sankey_fig.update_layout(title_text="Tier-to-Tier Movement (expected customers)", font_size=12)
st.plotly_chart(sankey_fig, use_container_width=True)

try:
    sankey_png = sankey_fig.to_image(format="png", scale=2)
    st.download_button("🖼️ Download Sankey as PNG", data=sankey_png, file_name="ecosystem_sankey.png", mime="image/png")
except Exception as e:
    st.info("PNG export requires `kaleido` (already in requirements).")

st.subheader("Revenue & Margin Dashboard")
colA, colB = st.columns(2)
with colA:
    bar_rev = px.bar(rev_df, x="tier", y="revenue", title="Expected Revenue by Tier")
    st.plotly_chart(bar_rev, use_container_width=True)
    try:
        png = bar_rev.to_image(format="png", scale=2)
        st.download_button("🖼️ Download Revenue chart", data=png, file_name="revenue_by_tier.png", mime="image/png")
    except Exception:
        pass
with colB:
    bar_contrib = px.bar(rev_df, x="tier", y="contribution", title="Contribution Margin by Tier",
                         hover_data=["avg_margin_pct"])
    st.plotly_chart(bar_contrib, use_container_width=True)
    try:
        png2 = bar_contrib.to_image(format="png", scale=2)
        st.download_button("🖼️ Download Margin chart", data=png2, file_name="contribution_by_tier.png", mime="image/png")
    except Exception:
        pass

st.dataframe(rev_df.round(2), use_container_width=True)

st.markdown("---")
st.subheader("Mermaid Map (copy-paste to your wiki)")
mermaid_lines = ["graph LR"]
class_defs = [
    'classDef entry fill:#d6f5d6,stroke:#333,stroke-width:1px;',
    'classDef core fill:#b3d9ff,stroke:#333,stroke-width:1px;',
    'classDef premium fill:#ffcccc,stroke:#333,stroke-width:1px;',
    'classDef upsell fill:#fff0b3,stroke:#333,stroke-width:1px;',
    'classDef recurring fill:#e6ccff,stroke:#333,stroke-width:1px;'
]
id_map = {"Entry":"A","Core":"B","Premium":"C","Upsell":"D","Recurring":"E"}
for _, r in flows.iterrows():
    s = id_map.get(r["source_tier"], "A")
    t = id_map.get(r["target_tier"], "B")
    lab = r.get("label","")
    mermaid_lines.append(f"    {s}[{r['source_tier']} Offers] -->|{lab}| {t}[{r['target_tier']} Offers]")
for t, code in id_map.items():
    cls = t.lower()
    mermaid_lines.append(f"    {code}:::{cls}")
mermaid_lines += [""] + [f"classDef {c}" for c in ["entry fill:#d6f5d6,stroke:#333,stroke-width:1px;",
                                                   "core fill:#b3d9ff,stroke:#333,stroke-width:1px;",
                                                   "premium fill:#ffcccc,stroke:#333,stroke-width:1px;",
                                                   "upsell fill:#fff0b3,stroke:#333,stroke-width:1px;",
                                                   "recurring fill:#e6ccff,stroke:#333,stroke-width:1px;"]]
mermaid_code = "\n".join(mermaid_lines)
st.code(mermaid_code, language="mermaid")
st.download_button("⬇️ Download Mermaid (.md)", data=f"```mermaid\n{mermaid_code}\n```", file_name="offer_ecosystem_mermaid.md")

st.markdown("---")
st.subheader("Customer Psychology (Anchoring · Scarcity · Positioning)")
psych = offers[["offer","tier","anchor","scarcity","positioning_frame","notes"]].copy()
st.dataframe(psych, use_container_width=True)

anchor_list = offers[offers["anchor"]]["offer"].tolist()
scarce_list = offers[offers["scarcity"]]["offer"].tolist()
st.write("**Anchors (set the frame):** ", ", ".join(anchor_list) if anchor_list else "None")
st.write("**Scarcity/Exclusivity:** ", ", ".join(scarce_list) if scarce_list else "None")

st.markdown("---")
st.subheader("ERRC Grid (Eliminate · Reduce · Raise · Create)")
mix = rev_df.set_index("tier")["revenue"]
mix = mix / mix.sum() if mix.sum() > 0 else mix
auto = []
for _, r in offers.iterrows():
    tier = r["tier"]
    margin = r["margin_pct"]
    revenue_share = float(mix.get(tier, 0.0))
    if tier=="Entry" and margin < 0.3 and revenue_share==0:
        action = "Create"
        rationale = "Make Entry irresistible (specific problem, genuine lead magnet)."
    elif margin < 0.4 and tier!="Recurring":
        action = "Reduce"
        rationale = "Low margin; streamline delivery or reposition."
    elif tier in ["Core","Recurring"] and revenue_share < 0.2:
        action = "Raise"
        rationale = "Underweight for core/recurring; boost proof, packaging, or pathways."
    else:
        action = "Keep"
        rationale = "Healthy economics or strategic role."
    auto.append({"offer": r["offer"], "action": action, "rationale": rationale})

errc_auto = pd.DataFrame(auto)
errc_join = errc_auto.merge(errc, on="offer", how="left", suffixes=("_auto",""))
errc_join["action"] = errc_join["action"].fillna(errc_join["action_auto"])
errc_join["rationale"] = errc_join["rationale"].fillna(errc_join["rationale_auto"])
errc_view = errc_join[["offer","action","rationale"]].copy()

errc_edit = st.data_editor(
    errc_view, num_rows="dynamic", use_container_width=True,
    column_config={"action": st.column_config.SelectboxColumn("action", options=["Eliminate","Reduce","Raise","Create","Keep"])}
)
st.download_button("⬇️ Download ERRC (CSV)", data=errc_edit.to_csv(index=False), file_name="errc_grid.csv", mime="text/csv")

st.markdown("---")
st.subheader("Positioning Narrative & Recurring Pathway Plan")
top_core = offers[offers["tier"]=="Core"]["offer"].tolist()
top_premium = offers[offers["tier"]=="Premium"]["offer"].tolist()
retainers = offers[(offers["tier"]=="Recurring") & (offers["mrr"]>0)]["offer"].tolist()
anchor_list = offers[offers["anchor"]]["offer"].tolist()
scarce_list = offers[offers["scarcity"]]["offer"].tolist()
narr = []
narr.append("**Positioning Narrative**")
narr.append(f"- Core is framed against competitor weaknesses via: {', '.join(top_core) if top_core else 'N/A'}")
narr.append(f"- Premium anchors value perception via: {', '.join(top_premium) if top_premium else 'N/A'}")
narr.append(f"- Psychological levers — Anchors: {', '.join(anchor_list) if anchor_list else 'None'}; Scarcity: {', '.join(scarce_list) if scarce_list else 'None'}")
narr.append("")
narr.append("**Recurring Pathway Plan**")
narr.append(f"- Post-Core retainer: {', '.join(retainers) if retainers else 'Define a default retainer'}")
narr.append("- Bowtie: Acquisition → Conversion → Expansion → Retention → Recurring")
narr.append("- Make recurring the default next step with explicit handoffs in Core/Premium playbooks.")
narr_md = "\n".join(narr)
st.markdown(narr_md)
st.download_button("⬇️ Download Narrative (Markdown)", data=narr_md, file_name="ecosystem_narrative.md", mime="text/markdown")

with st.sidebar.expander("Google Sheets (optional)", expanded=False):
    st.caption("Secrets: 'gcp_service_account' (JSON) and 'gsheets.url'. Tabs: offers, flows, errc.")
    load_btn = st.button("Load tables")
    save_btn = st.button("Save tables")

def _get_ws(url, title="data"):
    import gspread
    from google.oauth2.service_account import Credentials
    sa = st.secrets.get("gcp_service_account")
    if not sa or not st.secrets.get("gsheets", {}).get("url"):
        raise RuntimeError("Missing secrets: 'gcp_service_account' and/or 'gsheets.url'.")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(sa, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(st.secrets["gsheets"]["url"])
    try:
        ws = sh.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=title, rows="1000", cols="26")
    return ws

def _df_to_ws(ws, df_in):
    values = [list(df_in.columns)] + df_in.astype(object).where(pd.notnull(df_in), "").values.tolist()
    ws.clear()
    ws.update(values)

def _ws_to_df(ws):
    rows = ws.get_all_values()
    if not rows: return pd.DataFrame()
    hdr, data = rows[0], rows[1:]
    return pd.DataFrame(data, columns=hdr)

if 'load_btn' in locals() and load_btn:
    try:
        ws1 = _get_ws(st.secrets["gsheets"]["url"], "offers")
        ws2 = _get_ws(st.secrets["gsheets"]["url"], "flows")
        ws3 = _get_ws(st.secrets["gsheets"]["url"], "errc")
        offers = _ws_to_df(ws1); flows = _ws_to_df(ws2); errc = _ws_to_df(ws3)
        for c in ["price","mrr","term_months","margin_pct"]:
            if c in offers.columns: offers[c] = pd.to_numeric(offers[c], errors="coerce")
        if "prob" in flows.columns: flows["prob"] = pd.to_numeric(flows["prob"], errors="coerce")
        st.success("Loaded from Google Sheets.")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Load failed: {e}")

if 'save_btn' in locals() and save_btn:
    try:
        ws1 = _get_ws(st.secrets["gsheets"]["url"], "offers"); _df_to_ws(ws1, offers)
        ws2 = _get_ws(st.secrets["gsheets"]["url"], "flows");  _df_to_ws(ws2, flows)
        ws3 = _get_ws(st.secrets["gsheets"]["url"], "errc");   _df_to_ws(ws3, errc_edit)
        st.success("Saved to Google Sheets.")
    except Exception as e:
        st.error(f"Save failed: {e}")
