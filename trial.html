import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(
    page_title="Margin & Funnel Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Force dark mode (optional) ---
# Uncomment the next line to ALWAYS use dark mode
# st.markdown('<style>[data-testid="stAppViewContainer"] { background-color: #0e1117; }</style>', unsafe_allow_html=True)

# --- Title ---
st.title("📊 Margin Analysis & Funnel Diagnostics")
st.markdown("Interactive dashboard for margin, CAC/LTV, and funnel conversion analysis.")

# --- Sidebar for file upload ---
st.sidebar.header("📁 Data Input")
uploaded_file = st.sidebar.file_uploader("Upload client_revenue.csv", type=["csv"])

# --- Default sample data (if no file uploaded) ---
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # Create sample data for demo
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

# --- Margin Analysis ---
st.subheader("1. Margin Analysis")
df["gross_margin"] = (df["revenue"] - df["cogs"]) / df["revenue"]
df["contribution_margin"] = (df["revenue"] - df["cogs"] - df["channel_costs"]) / df["revenue"]

summary = df.groupby("product")[["gross_margin", "contribution_margin"]].mean().reset_index()
summary["gross_margin"] = summary["gross_margin"].round(3)
summary["contribution_margin"] = summary["contribution_margin"].round(3)

st.dataframe(summary.style.format("{:.1%}"), use_container_width=True)

# Optional: Bar chart
fig1 = px.bar(
    summary.melt(id_vars="product", var_name="Margin Type", value_name="Margin"),
    x="product",
    y="Margin",
    color="Margin Type",
    barmode="group",
    title="Average Margins by Product"
)
fig1.update_layout(yaxis_tickformat=".0%")
st.plotly_chart(fig1, use_container_width=True)

# --- CAC & LTV Calculator ---
st.subheader("2. CAC & LTV Analysis")
df["CAC"] = df["spend"] / df["customers_acquired"]
df["LTV"] = df["revenue_per_customer"] / df["churn_rate"]
df["LTV_CAC"] = df["LTV"] / df["CAC"]

ltv_cac_summary = df[["CAC", "LTV", "LTV_CAC"]].mean().to_frame().T.round(2)
st.dataframe(ltv_cac_summary, use_container_width=True)

# --- Funnel Conversion Diagnostic ---
st.subheader("3. Funnel Conversion Diagnostic")

# Allow user to input funnel stages
st.sidebar.markdown("---")
st.sidebar.subheader("Funnel Stages (Default)")
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

# Optional: Funnel chart
funnel_data = pd.DataFrame({
    "Stage": stage_names,
    "Count": [stages[s] for s in stage_names]
})
fig2 = px.funnel(funnel_data, x="Count", y="Stage", title="Sales Funnel")
st.plotly_chart(fig2, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("Built with Streamlit • Dark mode supported")
