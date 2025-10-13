import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Next Best Alternative Simulator", layout="wide")

st.title("Next Best Alternative Simulator")
st.caption("Compare your offer vs substitutes on Price and Effectiveness.")

# Sidebar: Data input
st.sidebar.header("Add Alternatives")
num_subs = st.sidebar.number_input("Number of Substitutes", 1, 10, 3)

alternatives = []
for i in range(num_subs):
    name = st.sidebar.text_input(f"Name {i+1}", f"Substitute {i+1}")
    price = st.sidebar.number_input(f"Price {i+1} ($)", 0, 10000, 100*(i+1))
    value = st.sidebar.slider(f"Effectiveness {i+1} (1–10)", 1, 10, 5)
    alternatives.append([name, price, value])

# Add client offer
offer_price = st.sidebar.number_input("Your Offer Price ($)", 0, 50000, 5000)
offer_value = st.sidebar.slider("Your Offer Effectiveness (1–10)", 1, 10, 8)
alternatives.append(["Your Offer", offer_price, offer_value])

df = pd.DataFrame(alternatives, columns=["Option", "Price", "Effectiveness"])
df["Value/Price Score"] = df["Effectiveness"] / df["Price"].replace(0, 1)

# Display data
st.subheader("Comparison Table")
st.dataframe(df, use_container_width=True)

# Chart: Price vs Effectiveness
fig = px.scatter(df, x="Price", y="Effectiveness", text="Option",
                 size="Value/Price Score", color="Option",
                 title="Price vs Effectiveness (Bigger = Better Value)")
fig.update_traces(textposition="top center")
st.plotly_chart(fig, use_container_width=True)

# Save option
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Results as CSV", csv, "substitutes.csv", "text/csv")
