import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Anchor Effect Calculator", layout="wide")

st.title("Anchor Effect Calculator")
st.caption("See how your offer looks when benchmarked against substitutes, competitors, and premiums.")

# Inputs
st.sidebar.header("Input Prices")
sub_price = st.sidebar.number_input("Substitute Price ($)", min_value=0, value=50)
comp_price = st.sidebar.number_input("Competitor Price ($)", min_value=0, value=500)
premium_price = st.sidebar.number_input("Premium Benchmark ($)", min_value=0, value=5000)
offer_price = st.sidebar.number_input("Your Offer Price ($)", min_value=0, value=2000)

# Bargain index
bargain_index = 1 - (offer_price - sub_price) / max((premium_price - sub_price), 1)
bargain_index = round(bargain_index, 2)

# Display metrics
st.subheader("Perceived Bargain Factor")
st.metric(label="Bargain Index (0–1)", value=bargain_index)

# Chart
fig = go.Figure()

# Range line
fig.add_trace(go.Scatter(x=[sub_price, premium_price], y=[0, 0],
                         mode="lines", line=dict(color="lightgray", width=4),
                         showlegend=False))

# Points
points = {
    "Substitute": sub_price,
    "Competitor": comp_price,
    "Your Offer": offer_price,
    "Premium": premium_price
}

colors = {
    "Substitute": "red",
    "Competitor": "orange",
    "Your Offer": "green",
    "Premium": "blue"
}

for label, price in points.items():
    fig.add_trace(go.Scatter(
        x=[price], y=[0],
        mode="markers+text",
        marker=dict(size=14, color=colors[label]),
        text=[label + f" (${price})"],
        textposition="top center",
        name=label
    ))

fig.update_layout(title="Anchor Effect Spectrum",
                  xaxis_title="Price ($)",
                  yaxis_visible=False,
                  showlegend=False)

st.plotly_chart(fig, use_container_width=True)
