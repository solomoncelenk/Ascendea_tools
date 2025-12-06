import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Ascendea Pricing Architecture Auditor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ASCENDEA THEME (GLOBAL CSS INJECTION) ---
ASCENDEA_CSS = """
<style>
:root {
  --asc-bg: #02030a;
  --asc-bg-soft: #0b1020;
  --asc-text: #ffffff;
  --asc-text-soft: rgba(255,255,255,0.72);
  --asc-brand: #f2003c;
  --asc-info: #00e4ab;
  --asc-card-bg: rgba(8,11,24,0.96);
  --asc-card-border: rgba(255,255,255,0.14);
  --asc-shadow:
    0 28px 90px rgba(0,0,0,0.9),
    0 0 0 1px rgba(255,255,255,0.02);
  --asc-radius: 18px;
}

/* App background */
[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(circle at 10% 0%, rgba(0,228,171,0.21) 0, transparent 48%),
    radial-gradient(circle at 90% 100%, rgba(242,0,60,0.25) 0, transparent 55%),
    radial-gradient(circle at 50% 20%, #151a30 0, #050814 60%, #000000 100%);
  color: var(--asc-text);
}

/* Main layout container */
.block-container {
  padding-top: 2.4rem;
  padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #050814 0%, #03040b 60%, #000000 100%);
  border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * {
  color: var(--asc-text-soft) !important;
}

/* Generic "card" wrapper */
.asc-section {
  background:
    radial-gradient(circle at 0% 0%, rgba(0,228,171,0.12) 0, transparent 55%),
    radial-gradient(circle at 100% 100%, rgba(242,0,60,0.12) 0, transparent 55%),
    var(--asc-card-bg);
  border-radius: var(--asc-radius);
  border: 1px solid var(--asc-card-border);
  box-shadow: var(--asc-shadow);
  padding: 22px 22px 18px;
  margin-bottom: 18px;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

/* Titles */
h1, h2, h3 {
  font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #ffffff;
}

h1 {
  font-size: 1.8rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 0.2rem;
}

.asc-kicker {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.22em;
  color: rgba(255,255,255,0.55);
  margin-bottom: 0.2rem;
}

.asc-subtitle {
  font-size: 0.95rem;
  color: var(--asc-text-soft);
  max-width: 620px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  gap: 6px;
  border-bottom: 1px solid rgba(255,255,255,0.18);
}
.stTabs [data-baseweb="tab"] {
  background-color: rgba(10,12,26,0.96);
  border-radius: 999px 999px 0 0;
  padding-top: 6px;
  padding-bottom: 6px;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--asc-info), #5bffcf);
  color: #0a1016 !important;
}

/* Data editor / tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.16);
  background-color: rgba(6,10,22,0.96);
}

/* Inputs and widgets */
.stTextInput > div > div > input,
.stNumberInput input,
.stTextArea textarea {
  background-color: rgba(6,10,22,0.96);
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.18);
  color: #ffffff;
}
.stTextArea textarea {
  border-radius: 14px;
}

/* Buttons */
.stButton button {
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.2);
  background-color: rgba(16,22,48,0.96);
  color: rgba(255,255,255,0.92);
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}
.stButton button:hover {
  border-color: var(--asc-info);
  background-color: rgba(25,33,72,0.96);
}

/* Download button */
[data-testid="baseButton-secondary"] {
  border-radius: 999px !important;
}

/* Plotly container padding */
.element-container:has(.js-plotly-plot) {
  padding: 6px 2px 0 2px;
}

/* Markdown text */
p {
  color: var(--asc-text-soft);
}
</style>
"""

st.markdown(ASCENDEA_CSS, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def generate_vrio_summary(df: pd.DataFrame) -> str:
    """Generates a markdown summary for the VRIO assessment."""
    if df.empty:
        return ""

    strong_advantages = df[df["VRIO Score"] == "Sustainable Competitive Advantage (V, R, I, O)"]
    weak_points = df[df["VRIO Score"].isin([
        "Competitive Parity (V)",
        "Temporary Competitive Advantage (V, R)",
        "Temporary Competitive Advantage (V, R, I)",
    ])]

    summary = "### VRIO Assessment Summary\n"

    if not strong_advantages.empty:
        summary += (
            "**Sustainable Competitive Advantage (V, R, I, O):** These are your most powerful advantages – "
            "Valuable, Rare, Inimitable, and Organized to capture. They underpin long-term pricing power.\n\n"
            "* **Key Strengths:** " + ", ".join(strong_advantages["Resource/Capability"].tolist()) + "\n"
        )
    else:
        summary += (
            "* **No Sustainable Advantages Identified:** Focus on improving Rarity, Inimitability, or "
            "Organisational support for current capabilities.\n"
        )

    if not weak_points.empty:
        summary += (
            "\n**Areas for Improvement (Below Sustainable):** These require strengthening to prevent "
            "competitive erosion.\n"
            "* **To Enhance:** " + ", ".join(weak_points["Resource/Capability"].tolist()) + "\n"
        )

    return summary


# --- HEADER / HOOK ---
header_col1, header_col2 = st.columns([2.5, 1.5])

with header_col1:
    st.markdown(
        """
        <div class="asc-kicker">Ascendea Revenue Model Intensive</div>
        <h1>Pricing Architecture Map</h1>
        <div class="asc-subtitle">
        The internal tool we use to structure pricing inside a Revenue Model Intensive. 
        Start with a clear pricing map. Then test the strength of your advantages.
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_col2:
    st.markdown(
        """
        <div class="asc-section" style="padding: 14px 16px 12px; margin-bottom: 0;">
          <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.18em; opacity:0.7;">
            Session Context
          </div>
          <div style="margin-top:4px; font-size:0.9rem; opacity:0.9;">
            Use this during a Revenue Model Intensive to map floors, baselines, and ceilings before re-architecting your pricing.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

# --- STEP 1: PRICING MAP DEFINITION (Direct, Substitutes, Premium) ---
with st.container():
    st.markdown('<div class="asc-section">', unsafe_allow_html=True)

    st.subheader("1. Pricing Architecture Map Definition")
    st.markdown(
        """
        The map is structured around three layers that define the **floor customers default to**, the **baseline they expect**, 
        and the **credible ceiling** your offer can support.
        """
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Direct Competitors (Baseline)",
            "Substitutes / Alternatives (Floor)",
            "Premium Benchmarks (Ceiling)",
        ]
    )

    with tab1:
        st.markdown("#### Direct Competitors: Baseline")
        st.info(
            "Direct competitors define the **baseline buyers expect** and anchor the perceived value of your core offering."
        )
        if "direct_competitors" not in st.session_state:
            st.session_state.direct_competitors = pd.DataFrame(
                {
                    "Name": ["Comp A", "Comp B"],
                    "Offering": ["Standard Service", "Premium Package"],
                    "Price ($)": [5000, 10000],
                }
            )
        st.session_state.direct_competitors = st.data_editor(
            st.session_state.direct_competitors,
            num_rows="dynamic",
            use_container_width=True,
        )

    with tab2:
        st.markdown("#### Substitutes / Alternatives: Floor")
        st.info(
            "Substitutes reveal the **functional floor** customers default to when your offer is not present "
            "(DIY, internal hires, courses, generic agencies)."
        )
        if "substitutes" not in st.session_state:
            st.session_state.substitutes = pd.DataFrame(
                {
                    "Name": ["DIY Course", "Internal Hire (Cost)"],
                    "Offering": ["Self-serve solution", "Annual FTE salary equivalent"],
                    "Price ($)": [500, 120000],
                }
            )
        st.session_state.substitutes = st.data_editor(
            st.session_state.substitutes,
            num_rows="dynamic",
            use_container_width=True,
        )

    with tab3:
        st.markdown("#### Premium Benchmarks: Ceiling")
        st.info(
            "Premium benchmarks **set the headroom** available in the market and define the upper band of credible premium value."
        )
        if "premium_benchmarks" not in st.session_state:
            st.session_state.premium_benchmarks = pd.DataFrame(
                {
                    "Name": ["Elite Consultant", "High-Calibre Program"],
                    "Offering": ["Executive Advisory", "High-Touch Accelerator"],
                    "Price ($)": [35000, 50000],
                }
            )
        st.session_state.premium_benchmarks = st.data_editor(
            st.session_state.premium_benchmarks,
            num_rows="dynamic",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# --- STEP 2: STRATEGIC ANALYSIS (VRIO & BLUE OCEAN) ---
with st.container():
    st.markdown('<div class="asc-section">', unsafe_allow_html=True)

    st.subheader("2. Strategic Analysis (VRIO & Value Curve)")
    st.markdown(
        """
        Once we know the pricing lanes in the market, we test **where your pricing power comes from** – 
        the assets you hold that competitors cannot easily match and how they show up in the value curve.
        """
    )

    # 2.1 VRIO Assessment
    st.markdown("##### VRIO Assessment: Strength of Advantages")
    st.markdown(
        """
        Assess each resource or capability against **Valuable, Rare, Inimitable, and Organised**. 
        The goal is to surface which elements truly justify premium pricing and which need strengthening.
        """
    )

    vrio_scores = [
        "Competitive Disadvantage (No V)",
        "Competitive Parity (V)",
        "Temporary Competitive Advantage (V, R)",
        "Temporary Competitive Advantage (V, R, I)",
        "Sustainable Competitive Advantage (V, R, I, O)",
    ]
    vrio_mapping = {
        "Resource/Capability": st.column_config.TextColumn(
            "Resource / Capability", required=True
        ),
        "VRIO Score": st.column_config.SelectboxColumn(
            "VRIO Score", options=vrio_scores, required=True
        ),
        "Notes": st.column_config.TextColumn("Notes", required=False),
    }

    if "vrio_analysis" not in st.session_state:
        st.session_state.vrio_analysis = pd.DataFrame(
            {
                "Resource/Capability": [
                    "Proprietary Process",
                    "Team Expertise",
                    "Client Network",
                ],
                "VRIO Score": [
                    "Sustainable Competitive Advantage (V, R, I, O)",
                    "Temporary Competitive Advantage (V, R)",
                    "Competitive Parity (V)",
                ],
                "Notes": [
                    "Codified, difficult to copy",
                    "High turnover risk",
                    "Standard for the industry",
                ],
            }
        )

    st.session_state.vrio_analysis = st.data_editor(
        st.session_state.vrio_analysis,
        column_config=vrio_mapping,
        num_rows="dynamic",
        key="vrio_editor",
        use_container_width=True,
    )

    st.markdown(generate_vrio_summary(st.session_state.vrio_analysis))

    st.markdown("---")

    # 2.2 Blue Ocean Value Curve (Simplified)
    st.markdown("##### Value Curve: Visualising Differentiation")
    st.markdown(
        """
        Score your offer against the industry on the factors buyers actually feel. 
        This creates a simple value curve you can point to in the room when repositioning price.
        """
    )

    if "value_factors" not in st.session_state:
        st.session_state.value_factors = pd.DataFrame(
            {
                "Factor": [
                    "Speed of Delivery",
                    "Customisation Level",
                    "Post-Service Support",
                    "Price",
                ],
                "Your Offering": [8, 9, 7, 5],
                "Industry Standard": [5, 5, 5, 5],
            }
        )

    st.session_state.value_factors = st.data_editor(
        st.session_state.value_factors,
        column_config={
            "Factor": st.column_config.TextColumn("Key Value Factor"),
            "Your Offering": st.column_config.NumberColumn(
                "Your Offering (1–10)", min_value=1, max_value=10, step=1
            ),
            "Industry Standard": st.column_config.NumberColumn(
                "Industry Standard (1–10)", min_value=1, max_value=10, step=1
            ),
        },
        num_rows="dynamic",
        key="blue_ocean_editor",
        use_container_width=True,
    )

    if not st.session_state.value_factors.empty:
        df_plot = st.session_state.value_factors.melt(
            id_vars="Factor", var_name="Curve", value_name="Score"
        )
        fig = px.line(
            df_plot,
            x="Factor",
            y="Score",
            color="Curve",
            markers=True,
            title="Value Curve – Your Offer vs Industry",
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, system-ui", color="#ffffff"),
            xaxis_title="Key Value Factors",
            yaxis_title="Score (1–10)",
            legend_title="Curve",
            hovermode="x unified",
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.12)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# --- STEP 3: CONSOLIDATED REPORT & PLAYBOOK ---
with st.container():
    st.markdown('<div class="asc-section">', unsafe_allow_html=True)

    st.subheader("3. Consolidated Report & Playbook")
    st.markdown(
        """
        The final layer joins the map, the VRIO assessment, and the value curve into a single narrative: 
        where your pricing floor sits, where you can anchor the core offer, and how high you can credibly push premium tiers.
        """
    )

    # Prepare Pricing Data for Visualisation
    all_pricing = pd.concat(
        [
            st.session_state.direct_competitors.assign(
                Category="Direct Competitors (Baseline)"
            ),
            st.session_state.substitutes.assign(
                Category="Substitutes (Floor)"
            ),
            st.session_state.premium_benchmarks.assign(
                Category="Premium Benchmarks (Ceiling)"
            ),
        ],
        ignore_index=True,
    )

    if not all_pricing.empty and "Price ($)" in all_pricing.columns:
        st.markdown("##### Price Distribution Across Market Categories")
        pricing_fig = px.scatter(
            all_pricing,
            x="Price ($)",
            y="Category",
            color="Category",
            size="Price ($)",
            hover_data=["Name", "Offering"],
            title="Market Positioning and Pricing Zones",
        )
        pricing_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, system-ui", color="#ffffff"),
            yaxis_title="Market Category",
            xaxis_title="Price",
            xaxis_tickprefix="$",
            legend_title="Category",
        )
        pricing_fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.12)")
        pricing_fig.update_yaxes(showgrid=False)
        st.plotly_chart(pricing_fig, use_container_width=True)

    st.markdown("##### Pricing Architecture Playbook Synthesis")
    st.markdown(
        """
        Capture the key decisions and moves from this session. 
        This becomes the reference point for tiering, anchoring, and future price moves.
        """
    )

    # Final playbook text area
    if not all_pricing.empty and "Price ($)" in all_pricing.columns:
        floor_avg = all_pricing[
            all_pricing["Category"] == "Substitutes (Floor)"
        ]["Price ($)"].mean()
        baseline_min = all_pricing[
            all_pricing["Category"] == "Direct Competitors (Baseline)"
        ]["Price ($)"].min()
        baseline_max = all_pricing[
            all_pricing["Category"] == "Direct Competitors (Baseline)"
        ]["Price ($)"].max()
        ceiling_max = all_pricing[
            all_pricing["Category"] == "Premium Benchmarks (Ceiling)"
        ]["Price ($)"].max()
    else:
        floor_avg = baseline_min = baseline_max = ceiling_max = 0.0

    final_playbook = st.text_area(
        "**Definitive Playbook Notes (Actionable Advice)**",
        height=260,
        value=f"""
**Client: [Insert Client Name]**  
**Date: {datetime.now().strftime('%Y-%m-%d')}**

### 1. Pricing Floor and Ceiling
* **Pricing Floor (Substitutes):** The average price of substitutes is ${floor_avg:.2f}. The core offer should not undercut this without a deliberate scope reduction.
* **Expected Baseline (Direct Competitors):** The competitive range runs from ${baseline_min:.2f} to ${baseline_max:.2f}. Position the flagship offer in this band unless the value curve and VRIO justify a higher anchor.
* **Credible Ceiling (Premium Benchmarks):** The credible ceiling is around ${ceiling_max:.2f}. Premium tiers should cluster here, supported by your strongest VRIO-backed advantages.

### 2. Protecting Pricing Power (VRIO)
* **Key Advantage(s) to Leverage:** [Reference 1–2 sustainable advantages from the VRIO summary that clearly justify premium pricing.]
* **Pricing Strategy Recommendation:** [Based on the value curve, specify the strategy – e.g. premium pricing with strong anchor, tiered structure with decoy, or staged elevation from current baseline.]

### 3. Next Steps (Architecture Development)
* [Define specific moves for tier packaging, feature fencing, and value-metric selection.]
* [Outline required changes to offers, terms, or delivery model to support the new architecture.]
""",
    )

    st.markdown("---")

    # --- SAVE/EXPORT BUTTON ---
    export_md = (
        f"# Pricing Architecture Audit Report\n\n"
        f"## Client: [Client Name]\n"
        f"## Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        f"### 1. Pricing Map\n\n"
        f"#### Direct Competitors (Baseline)\n"
        f"{st.session_state.direct_competitors.to_markdown(index=False)}\n\n"
        f"#### Substitutes (Floor)\n"
        f"{st.session_state.substitutes.to_markdown(index=False)}\n\n"
        f"#### Premium Benchmarks (Ceiling)\n"
        f"{st.session_state.premium_benchmarks.to_markdown(index=False)}\n\n"
        f"### 2. Strategic Analysis (VRIO)\n\n"
        f"#### VRIO Assessment\n"
        f"{st.session_state.vrio_analysis.to_markdown(index=False)}\n\n"
        f"{generate_vrio_summary(st.session_state.vrio_analysis)}\n\n"
        f"### 3. Final Playbook Synthesis\n\n"
        f"{final_playbook}\n"
    )

    st.download_button(
        label="Download Full Audit Report (Markdown)",
        data=export_md,
        file_name=f"Ascendea_Pricing_Audit_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown",
    )

    st.markdown("</div>", unsafe_allow_html=True)


# --- SIDEBAR AUTHORITY CLOSE ---
st.sidebar.header("Ascendea Revenue Model Intensive")
st.sidebar.info(
    "This auditor sits inside the Revenue Model Intensive. "
    "Use it to map floors, baselines, and ceilings, then link pricing decisions back to VRIO-backed advantages."
)
