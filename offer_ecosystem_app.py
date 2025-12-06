import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_mermaid import mermaid  # for actual diagram rendering

px.defaults.template = "plotly_dark"

st.set_page_config(page_title="Offer Ecosystem Map", layout="wide")
st.title("Offer Ecosystem Map — Tiers, Flows, Finance & Strategy")

st.caption("Visualise Entry → Core → Premium → Upsell → Recurring, layer psychology, and run financial diagnostics.")

TIERS = ["Entry","Core","Premium","Upsell","Recurring"]

# -----------------------
# Sample data
# -----------------------
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
    "label": ["Low-friction lead in","Advance","Upsell","Retainer","Retainer","Retainer","Feeds"],
    "prob": [0.30, 0.35, 0.25, 0.70, 0.50, 0.80, 0.30],
    "notes": ["Entry→Core conversion","Core→Premium","Cross-sell rate","Premium to Retainer","Core to Retainer","Premium to Retainer","Entry→Core repeat"]
})

# -----------------------
# Sidebar data mode
# -----------------------
with st.sidebar:
    st.header("Data")
    mode = st.radio("Choose data mode", ["Manual editor", "Upload CSVs"], index=0)
    st.caption("Upload `offers.csv` and `flows.csv` (optional).")

def read_or_default(uploaded_list):
    frames = {"offers": None, "flows": None}
    sigs = {
        "offers": {"offer","tier","price","mrr","term_months","margin_pct","anchor","scarcity","positioning_frame","enabled","notes"},
        "flows": {"source_tier","target_tier","label","prob","notes"},
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
    return frames

if mode == "Upload CSVs":
    with st.sidebar:
        uploads = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)
    frames = read_or_default(uploads)
else:
    if "eco_frames" not in st.session_state:
        st.session_state.eco_frames = {
            "offers": sample_offers.copy(),
            "flows": sample_flows.copy(),
        }

    with st.sidebar:
        c1, c2 = st.columns(2)
        if c1.button("Reset to sample"):
            st.session_state.eco_frames = {
                "offers": sample_offers.copy(),
                "flows": sample_flows.copy(),
            }
        st.download_button(
            "⬇️ Download offers.csv",
            st.session_state.eco_frames["offers"].to_csv(index=False),
            "offers.csv",
            "text/csv"
        )
        st.download_button(
            "⬇️ Download flows.csv",
            st.session_state.eco_frames["flows"].to_csv(index=False),
            "flows.csv",
            "text/csv"
        )

    # Offers editor
    st.subheader("Offers (tiers & economics)")
    st.caption("Columns: tier (Entry/Core/Premium/Upsell/Recurring), price (one-time), mrr (monthly), term_months (recurring), margin_pct (0–1)")
    st.session_state.eco_frames["offers"] = st.data_editor(
        st.session_state.eco_frames["offers"],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "tier": st.column_config.SelectboxColumn("tier", options=TIERS),
            "margin_pct": st.column_config.NumberColumn("margin_pct", min_value=0.0, max_value=1.0, step=0.05),
            "enabled": st.column_config.CheckboxColumn("enabled", default=True),
            "anchor": st.column_config.CheckboxColumn("anchor", default=False),
            "scarcity": st.column_config.CheckboxColumn("scarcity", default=False),
        }
    )

    # Flows editor
    st.subheader("Flows (tier-level)")
    st.caption("Probabilities (0–1) define % moving from source → target per period/cohort.")
    st.session_state.eco_frames["flows"] = st.data_editor(
        st.session_state.eco_frames["flows"],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "source_tier": st.column_config.SelectboxColumn("source_tier", options=TIERS),
            "target_tier": st.column_config.SelectboxColumn("target_tier", options=TIERS),
            "prob": st.column_config.NumberColumn("prob", min_value=0.0, max_value=1.0, step=0.05)
        }
    )

    frames = st.session_state.eco_frames

offers = frames["offers"].copy()
flows  = frames["flows"].copy()

# -----------------------
# Assumptions
# -----------------------
with st.sidebar:
    st.header("Assumptions")
    cohort = st.number_input("Entry cohort size (customers)", min_value=0, value=1000, step=50)
    months = st.number_input("Recurring term for MRR (months)", min_value=1, value=12, step=1)

# -----------------------
# Clean + finance calc
# -----------------------
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
    outgoing = flow_matrix[flow_matrix["source_tier"] == src]
    for _, row in outgoing.iterrows():
        tgt = row["target_tier"]
        cust[tgt] += base * row["prob"]

rev = {}
rev_margin = {}
for _, row in tier_fin.iterrows():
    tier = row["tier"]
    customers = cust.get(tier, 0.0)
    one_time_revenue = customers * row["avg_price"]
    recurring_revenue = customers * row["avg_mrr"] * (
        months if tier != "Recurring"
        else row["avg_term"] if row["avg_term"] > 0
        else months
    )
    total_rev = one_time_revenue + recurring_revenue
    rev[tier] = total_rev
    rev_margin[tier] = total_rev * row["avg_margin"]

rev_df = pd.DataFrame({
    "tier": TIERS,
    "expected_customers": [cust[t] for t in TIERS],
    "revenue": [rev[t] for t in TIERS],
    "contribution": [rev_margin[t] for t in TIERS],
    "avg_margin_pct": [
        tier_fin[tier_fin['tier'] == t]["avg_margin"].values[0] if t in tier_fin["tier"].values else 0
        for t in TIERS
    ]
})

# -----------------------
# Sankey flow map
# -----------------------
st.markdown("---")
st.subheader("Flow Map (Sankey)")

links = flows.copy()
links = links.merge(
    pd.DataFrame({"tier": list(cust.keys()), "expected_customers": list(cust.values())}),
    left_on="source_tier",
    right_on="tier",
    how="left"
)
links["value"] = (links["prob"] * links["expected_customers"]).round(2)

labels = TIERS
lab_to_idx = {lab: i for i, lab in enumerate(labels)}
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
    st.download_button(
        "🖼️ Download Sankey as PNG",
        data=sankey_png,
        file_name="ecosystem_sankey.png",
        mime="image/png"
    )
except Exception:
    st.info("PNG export requires `kaleido` installed in the environment.")

# -----------------------
# Revenue & margin charts
# -----------------------
st.subheader("Revenue & Margin Dashboard")
colA, colB = st.columns(2)

with colA:
    bar_rev = px.bar(rev_df, x="tier", y="revenue", title="Expected Revenue by Tier")
    st.plotly_chart(bar_rev, use_container_width=True)
    try:
        png = bar_rev.to_image(format="png", scale=2)
        st.download_button(
            "🖼️ Download Revenue chart",
            data=png,
            file_name="revenue_by_tier.png",
            mime="image/png"
        )
    except Exception:
        pass

with colB:
    bar_contrib = px.bar(
        rev_df,
        x="tier",
        y="contribution",
        title="Contribution Margin by Tier",
        hover_data=["avg_margin_pct"]
    )
    st.plotly_chart(bar_contrib, use_container_width=True)
    try:
        png2 = bar_contrib.to_image(format="png", scale=2)
        st.download_button(
            "🖼️ Download Margin chart",
            data=png2,
            file_name="contribution_by_tier.png",
            mime="image/png"
        )
    except Exception:
        pass

st.dataframe(rev_df.round(2), use_container_width=True)

# -----------------------
# Mermaid map (rendered with streamlit-mermaid)
# -----------------------
st.markdown("---")
st.subheader("Offer Ecosystem Mermaid Map")

mermaid_lines = ["graph LR"]

id_map = {"Entry": "A", "Core": "B", "Premium": "C", "Upsell": "D", "Recurring": "E"}

# Edges from flows
for _, r in flows.iterrows():
    s = id_map.get(r["source_tier"], "A")
    t = id_map.get(r["target_tier"], "B")
    lab = str(r.get("label", ""))
    mermaid_lines.append(f'{s}["{r["source_tier"]} Offers"] -->|{lab}| {t}["{r["target_tier"]} Offers"]')

# Class assignments
for tier, code in id_map.items():
    cls = tier.lower()
    mermaid_lines.append(f"{code}:::{cls}")

# Class definitions
mermaid_lines.append("classDef entry fill:#d6f5d6,stroke:#333,stroke-width:1px;")
mermaid_lines.append("classDef core fill:#b3d9ff,stroke:#333,stroke-width:1px;")
mermaid_lines.append("classDef premium fill:#ffcccc,stroke:#333,stroke-width:1px;")
mermaid_lines.append("classDef upsell fill:#fff0b3,stroke:#333,stroke-width:1px;")
mermaid_lines.append("classDef recurring fill:#e6ccff,stroke:#333,stroke-width:1px;")

mermaid_code = "graph LR\n" + "\n".join(mermaid_lines[1:])  # ensure single 'graph LR' at top

# Render the diagram
mermaid(mermaid_code)

# Download as .md for Notion / wiki
st.download_button(
    "⬇️ Download Mermaid (.md)",
    data=f"```mermaid\n{mermaid_code}\n```",
    file_name="offer_ecosystem_mermaid.md",
    mime="text/markdown"
)

# -----------------------
# Psychology table
# -----------------------
st.markdown("---")
st.subheader("Customer Psychology (Anchoring · Scarcity · Positioning)")

psych = offers[["offer","tier","anchor","scarcity","positioning_frame","notes"]].copy()
st.dataframe(psych, use_container_width=True)

anchor_list = offers[offers["anchor"]]["offer"].tolist()
scarce_list = offers[offers["scarcity"]]["offer"].tolist()
st.write("**Anchors (set the frame):** ", ", ".join(anchor_list) if anchor_list else "None")
st.write("**Scarcity/Exclusivity:** ", ", ".join(scarce_list) if scarce_list else "None")

# -----------------------
# Narrative
# -----------------------
st.markdown("---")
st.subheader("Positioning Narrative & Recurring Pathway Plan")

top_core = offers[offers["tier"] == "Core"]["offer"].tolist()
top_premium = offers[offers["tier"] == "Premium"]["offer"].tolist()
retainers = offers[(offers["tier"] == "Recurring") & (offers["mrr"] > 0)]["offer"].tolist()
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

st.download_button(
    "⬇️ Download Narrative (Markdown)",
    data=narr_md,
    file_name="ecosystem_narrative.md",
    mime="text/markdown"
)
