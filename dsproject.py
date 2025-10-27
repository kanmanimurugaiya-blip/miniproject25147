import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Athletics ML Performance Dashboard", page_icon="🏃", layout="wide")

st.title("🏃 Athletics ML Performance Dashboard")
st.subheader("Simulate Athlete Data Automatically (No CSV Needed!)")

# Sidebar selections
st.sidebar.header("Select Athlete")
athletes = ["Alice", "Bob", "Charlie", "David", "Emma"]
athlete = st.sidebar.selectbox("Athlete Name", athletes)

st.sidebar.header("Select Event")
events = ["100m", "200m", "400m", "Long Jump", "High Jump"]
event = st.sidebar.selectbox("Event", events)

# Generate random data automatically
np.random.seed(len(athlete) + len(event))
data = {
    "Heart Rate": np.random.randint(120, 190, 10),
    "Calories": np.random.randint(200, 500, 10),
    "Reaction Time": np.round(np.random.uniform(0.10, 0.30, 10), 2),
    "Speed": np.round(np.random.uniform(8.5, 11.0, 10), 2),
}
df = pd.DataFrame(data)

# Display data
st.write(f"### {athlete}'s {event} Performance Data")
st.dataframe(df, use_container_width=True)

# Plot graphs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Heart Rate vs Speed")
    fig1 = px.scatter(df, x="Heart Rate", y="Speed", size="Calories", color="Reaction Time", title="Performance Scatter")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Heart Rate Distribution")
    fig2 = px.histogram(df, x="Heart Rate", nbins=10, title="Heart Rate Distribution")
    st.plotly_chart(fig2, use_container_width=True)

# Summary stats
st.subheader("📊 Summary Statistics")
st.write(df.describe())

st.markdown("---")
st.caption("Made with ❤️ by Kanmani Murugaiya | Powered by Streamlit")
