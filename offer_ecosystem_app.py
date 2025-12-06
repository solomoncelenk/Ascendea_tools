import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------
# Global visual defaults
# -----------------------
px.defaults.template = "plotly_dark"

ASC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="stApp"] {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* App background */
.stApp {
  background: #000000;
}

.main {
  background:
    radial-gradient(circle at 10% 0%, rgba(78,191,176,0.35) 0, transparent 45%),
    radial-gradient(circle at 90% 100%, rgba(242,0,60,0.35) 0, transparent 55%),
    radial-gradient(circle at 50% 20%, #151a30 0, #050814 60%, #000000 100%);
}

/* Layout */
.block-container {
  max-width: 1200px;
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

/* Headings & text */
h1, h2, h3, h4, h5, h6 {
  color: #ffffff;
}
p, span, label {
  color: rgba(255,255,255,0.88);
}

/* Cards */
.asc-card {
  border-radius: 24px;
  border: 1px solid rgba(255,255,255,0.16);
  background:
    radial-gradient(circle at 0% 0%, rgba(78,191,176,0.18) 0, transparent 55%),
    radial-gradient(circle at 100% 100%, rgba(242,0,60,0.18) 0, transparent 55%),
    rgba(7,10,24,0.96);
  padding: 1.5rem 1.75rem;
  box-shadow:
    0 26px 90px rgba(0,0,0,0.85),
    0 0 0 1px rgba(255,255,255,0.02);
  margin-bottom: 1.5rem;
}

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
  color: #ffffff;
}

.asc-title span {
  color: #00E4AB;
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

/* Buttons (Ascendea style) */
.stButton > button, .stDownloadButton > button {
  background: #00E4AB !important;
  color: #393939 !important;
  border: 1px solid #FFFDD1 !important;
  border-radius: 999px;
  padding: 0.45rem 1.3rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  box-shadow: 0 10px 30px rgba(0,0,0,0.45);
}
.stButton > button:hover, .stDownloadButton > button:hover {
  filter: brightness(1.05);
  box-shadow: 0 14px 40px rgba(0,0,0,0.65);
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
    font-size: 1.5rem;
  }
  .asc-subtitle {
    font-size: 0.9rem;
  }
}
</style>
"""

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="Offer Ecosystem Map", layout="wide")
st.markdown(ASC_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div class="asc-card">
      <div class="asc-eyebrow">Ascendea Revenue Architecture</div>
      <div class="asc-title">Offer Ecosystem <span>Map</span></div>
      <div class="asc-subtitle">
        Map Entry → Core → Premium → Upsell → Recurring, overlay movement, and read tier-level revenue &
        margin in one view.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

TIERS = ["Entry", "Core", "Premium", "Upsell", "Recurring"]

# -----------------------
# Sample data
# -----------------------
sample_offers = pd.DataFrame({
    "offer": ["Free Workshop", "Core Program", "Premium Advisory", "Cross-sell Addon", "Growth Retainer"],
    "tier": ["Entry", "Core", "Premium", "Upsell", "Recurring"],
    "price": [0, 15000, 60000, 5000, 0],
    "mrr": [0, 0, 0, 0, 8000],
    "term_months": [0, 0, 0, 0, 12],
    "margin_pct": [0.20, 0.55, 0.65, 0.60, 0.70],
    "anchor": [False, False, True, False, False],
    "scarcity": [False, False, True, True, False],
    "positioning_frame": ["Workshop", "Program", "Partnership", "Add-on", "Retainer"],
    "enabled": [True, True, True, True, True],
    "notes": ["Lead magnet", "Flagship delivery", "Exec-only tier", "Sold post-core", "Monthly subscription"],
})

sample_flows = pd.DataFrame({
    "source_tier": ["Entry", "Core", "Core", "Premium", "Core", "Premium", "Entry"],
    "target_tier": ["Core", "Premium", "Upsell", "Recurring", "Recurring", "Recurring", "Core"],
    "label": [
        "Low-friction lead in",
        "Advance",
        "Upsell",
        "Retainer",
        "Retainer",
        "Retainer",
        "Feeds",
    ],
    "prob": [0.30, 0.35, 0.25, 0.70, 0.50, 0.80, 0.30],
    "notes": [
        "Entry→Core conversion",
        "Core→Premium",
        "Cross-sell rate",
        "Premium to Retainer",
        "Core to Retainer",
        "Premium to Retainer",
        "Entry→Core repeat",
    ],
})

# -----------------------
# Sidebar – data mode
# -----------------------
with st.sidebar:
    st.header("Data")
    mode = st.radio("Choose data mode", ["Manual editor", "Upload CSVs"], index=0)
    st.caption("Upload `offers.csv` and `flows.csv` (optional).")


def read_or_default(uploaded_list):
    frames = {"offers": None, "flows": None}
    sigs = {
        "offers": {
            "offer", "tier", "price", "mrr", "term_months",
            "margin_pct", "anchor", "scarcity",
            "positioning_frame", "enabled", "notes",
        },
        "flows": {"source_tier", "target_tier", "label", "prob", "notes"},
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
    frames["flows"] = frames["flows"] or sample_flows.copy()
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
            "text/csv",
        )
        st.download_button(
            "⬇️ Download flows.csv",
            st.session_state.eco_frames["flows"].to_csv(index=False),
            "flows.csv",
            "text/csv",
        )

    # Offers editor
    st.subheader("Offers (tiers & economics)")
    st.caption(
        "tier (Entry/Core/Premium/Upsell/Recurring), price (one-time), "
        "mrr (monthly), term_months (recurring), margin_pct (0–1)"
    )
    st.session_state.eco_frames["offers"] = st.data_editor(
        st.session_state.eco_frames["offers"],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "tier": st.column_config.SelectboxColumn("tier", options=TIERS),
            "margin_pct": st.column_config.NumberColumn(
                "margin_pct", min_value=0.0, max_value=1.0, step=0.05
            ),
            "enabled": st.column_config.CheckboxColumn("enabled", default=True),
            "anchor": st.column_config.CheckboxColumn("anchor", default=False),
            "scarcity": st.column_config.CheckboxColumn("scarcity", default=False),
        },
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
            "prob": st.column_config.NumberColumn("prob", min_value=0.0, max_value=1.0, step=0.05),
        },
    )

    frames = st.session_state.eco_frames

offers = frames["offers"].copy()
flows = frames["flows"].copy()

# -----------------------
# Sidebar – assumptions
# -----------------------
with st.sidebar:
    st.header("Assumptions")
    cohort = st.number_input(
        "Entry cohort size (customers)", min_value=0, value=1000, step=50
    )
    months = st.number_input(
        "Recurring term for MRR (months)", min_value=1, value=12, step=1
    )

# -----------------------
# Clean + finance calc
# -----------------------
offers["enabled"] = offers["enabled"].astype(bool)
offers = offers[offers["enabled"]]
offers["tier"] = offers["tier"].astype(str)

for c in ["price", "mrr", "term_months", "margin_pct"]:
    offers[c] = pd.to_numeric(offers[c], errors="coerce").fillna(0.0)

flows["prob"] = pd.to_numeric(flows["prob"], errors="coerce").fillna(0.0)
flows = flows[
    flows["source_tier"].isin(TIERS) & flows["target_tier"].isin(TIERS)
]

tier_fin = (
    offers.groupby("tier")
    .agg(
        avg_price=("price", "mean"),
        avg_mrr=("mrr", "mean"),
        avg_term=("term_months", "mean"),
        avg_margin=("margin_pct", "mean"),
        n_offers=("offer", "count"),
    )
    .reindex(TIERS)
    .fillna(0.0)
    .reset_index()
)

cust = {t: 0.0 for t in TIERS}
cust["Entry"] = float(cohort)

flow_matrix = (
    flows.groupby(["source_tier", "target_tier"])["prob"]
    .sum()
    .clip(upper=1.0)
    .reset_index()
)

order = ["Entry", "Core", "Premium", "Upsell", "Recurring"]
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
        months
        if tier != "Recurring"
        else row["avg_term"]
        if row["avg_term"] > 0
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
        tier_fin[tier_fin["tier"] == t]["avg_margin"].values[0]
        if t in tier_fin["tier"].values
        else 0
        for t in TIERS
    ],
})

# -----------------------
# Branded Offer Ecosystem Map (Sankey)
# -----------------------
st.markdown("---")
st.subheader("Offer Ecosystem Map (Branded Flow)")

links = flows.copy()
links = links.merge(
    pd.DataFrame(
        {"tier": list(cust.keys()), "expected_customers": list(cust.values())}
    ),
    left_on="source_tier",
    right_on="tier",
    how="left",
)
links["value"] = (links["prob"] * links["expected_customers"]).round(2)

labels = TIERS
lab_to_idx = {lab: i for i, lab in enumerate(labels)}
source_idx = links["source_tier"].map(lab_to_idx).tolist()
target_idx = links["target_tier"].map(lab_to_idx).tolist()
values = links["value"].tolist()

# Brand node colours
node_colors = {
    "Entry":     "#00E4AB",  # teal
    "Core":      "#4F46E5",  # indigo-ish
    "Premium":   "#F2003C",  # red
    "Upsell":    "#fd7232",  # orange
    "Recurring": "#8B5CF6",  # purple
}
node_color_list = [node_colors.get(t, "#999999") for t in labels]

sankey_fig = go.Figure(
    data=[
        go.Sankey(
            arrangement="snap",
            node=dict(
                label=labels,
                pad=25,
                thickness=20,
                color=node_color_list,
            ),
            link=dict(
                source=source_idx,
                target=target_idx,
                value=values,
                label=links["label"],
                color="rgba(255,255,255,0.35)",
            ),
        )
    ]
)
sankey_fig.update_layout(
    title_text="Tier-to-Tier Movement (Expected Customers)",
    font=dict(family="Inter", size=12, color="#ffffff"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(sankey_fig, use_container_width=True)

try:
    sankey_png = sankey_fig.to_image(format="png", scale=2)
    st.download_button(
        "🖼️ Download Ecosystem Map (PNG)",
        data=sankey_png,
        file_name="offer_ecosystem_map.png",
        mime="image/png",
    )
except Exception:
    st.info("PNG export requires `kaleido` installed in the environment.")

# -----------------------
# Revenue & margin charts
# -----------------------
st.markdown("---")
st.subheader("Revenue & Margin Dashboard")

colA, colB = st.columns(2)

with colA:
    bar_rev = px.bar(
        rev_df, x="tier", y="revenue", title="Expected Revenue by Tier"
    )
    bar_rev.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7,10,24,1)",
        font_color="#ffffff",
    )
    st.plotly_chart(bar_rev, use_container_width=True)
    try:
        png = bar_rev.to_image(format="png", scale=2)
        st.download_button(
            "🖼️ Download Revenue chart",
            data=png,
            file_name="revenue_by_tier.png",
            mime="image/png",
        )
    except Exception:
        pass

with colB:
    bar_contrib = px.bar(
        rev_df,
        x="tier",
        y="contribution",
        title="Contribution Margin by Tier",
        hover_data=["avg_margin_pct"],
    )
    bar_contrib.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7,10,24,1)",
        font_color="#ffffff",
    )
    st.plotly_chart(bar_contrib, use_container_width=True)
    try:
        png2 = bar_contrib.to_image(format="png", scale=2)
        st.download_button(
            "🖼️ Download Margin chart",
            data=png2,
            file_name="contribution_by_tier.png",
            mime="image/png",
        )
    except Exception:
        pass

st.dataframe(rev_df.round(2), use_container_width=True)

# -----------------------
# Psychology table
# -----------------------
st.markdown("---")
st.subheader("Customer Psychology (Anchoring · Scarcity · Positioning)")

psych = offers[
    ["offer", "tier", "anchor", "scarcity", "positioning_frame", "notes"]
].copy()
st.dataframe(psych, use_container_width=True)

anchor_list = offers[offers["anchor"]]["offer"].tolist()
scarce_list = offers[offers["scarcity"]]["offer"].tolist()
st.write(
    "**Anchors (set the frame):** ",
    ", ".join(anchor_list) if anchor_list else "None",
)
st.write(
    "**Scarcity/Exclusivity:** ",
    ", ".join(scarce_list) if scarce_list else "None",
)

# -----------------------
# Narrative
# -----------------------
st.markdown("---")
st.subheader("Positioning Narrative & Recurring Pathway Plan")

top_core = offers[offers["tier"] == "Core"]["offer"].tolist()
top_premium = offers[offers["tier"] == "Premium"]["offer"].tolist()
retainers = offers[
    (offers["tier"] == "Recurring") & (offers["mrr"] > 0)
]["offer"].tolist()
anchor_list = offers[offers["anchor"]]["offer"].tolist()
scarce_list = offers[offers["scarcity"]]["offer"].tolist()

narr = []
narr.append("**Positioning Narrative**")
narr.append(
    f"- Core is framed against competitor weaknesses via: "
    f"{', '.join(top_core) if top_core else 'N/A'}"
)
narr.append(
    f"- Premium anchors value perception via: "
    f"{', '.join(top_premium) if top_premium else 'N/A'}"
)
narr.append(
    f"- Psychological levers — Anchors: "
    f"{', '.join(anchor_list) if anchor_list else 'None'}; "
    f"Scarcity: {', '.join(scarce_list) if scarce_list else 'None'}"
)
narr.append("")
narr.append("**Recurring Pathway Plan**")
narr.append(
    f"- Post-Core retainer: "
    f"{', '.join(retainers) if retainers else 'Define a default retainer'}"
)
narr.append("- Bowtie: Acquisition → Conversion → Expansion → Retention → Recurring")
narr.append(
    "- Make recurring the default next step with explicit handoffs in Core/Premium playbooks."
)

narr_md = "\n".join(narr)
st.markdown(narr_md)

st.download_button(
    "⬇️ Download Narrative (Markdown)",
    data=narr_md,
    file_name="ecosystem_narrative.md",
    mime="text/markdown",
)
