import streamlit as st
import pandas as pd
import plotly.express as px

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

/* Hero card */
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

# --- Page config ---
st.set_page_config(
    page_title="Margin & Funnel Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Ascendea styling
st.markdown(ASC_CSS, unsafe_allow_html=True)

# --- Hero header ---
st.markdown(
    """
    <div class="asc-card">
      <div class="asc-eyebrow">Ascendea Commercial Intelligence</div>
      <div class="asc-title">Margin & Funnel <span>Analytics</span></div>
      <div class="asc-subtitle">
        Diagnose margin strength, CAC vs LTV, and funnel conversion in one view so you can
        re-price, re-focus channels, and reset sales expectations.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar for file upload ---
st.sidebar.header("Data Input")
uploaded_file = st.sidebar.file_uploader("Upload client_revenue.csv", type=["csv"])

# --- Default sample data (if no file uploaded) ---
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.DataFrame({
        "product": ["A", "B", "A", "B", "A", "B"],
        "revenue": [1000, 1500, 1200, 1300, 1100, 1400],
        "cogs": [400, 600, 480, 520, 440, 560],
        "channel_costs": [100, 150, 120, 130, 110, 140],
        "spend": [500, 750, 600, 650, 550, 700],
        "customers_acquired": [50, 75, 60, 65, 55, 70],
        "revenue_per_customer": [20, 20, 20, 20, 20, 20],
        "churn_rate": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    })

# =======================
# 1. Margin Analysis
# =======================
st.subheader("1. Margin Analysis")

df["gross_margin"] = (df["revenue"] - df["cogs"]) / df["revenue"]
df["contribution_margin"] = (df["revenue"] - df["cogs"] - df["channel_costs"]) / df["revenue"]

summary = df.groupby("product")[["gross_margin", "contribution_margin"]].mean().reset_index()

# Create display-friendly percentage strings (no Styler to avoid errors)
summary_display = summary.copy()
for col in ["gross_margin", "contribution_margin"]:
    summary_display[col] = (summary_display[col] * 100).round(1).astype(str) + "%"

st.dataframe(summary_display, use_container_width=True)

# Branded bar chart
fig1 = px.bar(
    summary.melt(id_vars="product", var_name="Margin Type", value_name="Margin"),
    x="product",
    y="Margin",
    color="Margin Type",
    barmode="group",
    title="Average Margins by Product",
    color_discrete_sequence=["#00E4AB", "#F2003C"]  # teal for gross, red for contribution
)
fig1.update_layout(
    yaxis_tickformat=".0%",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(7,10,24,1)",
    font_color="#ffffff",
)
st.plotly_chart(fig1, use_container_width=True)

# =======================
# 2. CAC & LTV Analysis
# =======================
st.subheader("2. CAC & LTV Analysis")

df["CAC"] = df["spend"] / df["customers_acquired"]
df["LTV"] = df["revenue_per_customer"] / df["churn_rate"]
df["LTV_CAC"] = df["LTV"] / df["CAC"]

ltv_cac_summary = df[["CAC", "LTV", "LTV_CAC"]].mean().to_frame().T.round(2)
st.dataframe(ltv_cac_summary, use_container_width=True)

# =======================
# 3. Funnel Conversion Diagnostic
# =======================
st.subheader("3. Funnel Conversion Diagnostic")

# Allow user to input funnel stages
st.sidebar.markdown("---")
st.sidebar.subheader("Funnel Stages")

leads = st.sidebar.number_input("Leads", value=1000, min_value=0)
qualified = st.sidebar.number_input("Qualified", value=300, min_value=0)
proposals = st.sidebar.number_input("Proposals", value=100, min_value=0)
closed = st.sidebar.number_input("Closed Won", value=25, min_value=0)

stages = {"Leads": leads, "Qualified": qualified, "Proposals": proposals, "Closed": closed}
stage_names = list(stages.keys())
conversion_rates = {}

for i in range(1, len(stage_names)):
    prev = stage_names[i - 1]
    curr = stage_names[i]
    rate = stages[curr] / stages[prev] if stages[prev] > 0 else 0
    conversion_rates[f"{prev} → {curr}"] = rate

# Display funnel conversion rates
funnel_df = pd.DataFrame(list(conversion_rates.items()), columns=["Stage Transition", "Conversion Rate"])
funnel_df["Conversion Rate"] = funnel_df["Conversion Rate"].round(4)
st.dataframe(funnel_df.style.format({"Conversion Rate": "{:.1%}"}), use_container_width=True)

# Branded funnel chart
funnel_data = pd.DataFrame({
    "Stage": stage_names,
    "Count": [stages[s] for s in stage_names]
})
fig2 = px.funnel(
    funnel_data,
    x="Count",
    y="Stage",
    title="Sales Funnel",
    color="Stage",
    color_discrete_sequence=["#00E4AB", "#4F46E5", "#F2003C", "#fd7232"]  # teal, indigo, red, orange
)
fig2.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(7,10,24,1)",
    font_color="#ffffff",
)
st.plotly_chart(fig2, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("Built with Streamlit · Ascendea Margin & Funnel Intelligence")
