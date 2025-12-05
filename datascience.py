import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Athlete Dashboard", layout="wide", page_icon="🏃‍♂️")
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        border-radius: 12px;
        padding: 20px;
    }
    h1 {
        color: #0077b6;
        text-align: center;
        font-size: 2.5em;
    }
    p, .footer {
        text-align: center;
        color: #333;
    }
</style>
<div class="main">
    <h1>Athlete Performance Dashboard</h1>
    <p>Dataset Viewer + Injury Tracker + Event Comparison</p>
</div>
""", unsafe_allow_html=True)

# ---------- LOAD DATASET ----------
st.sidebar.header("Upload Dataset")
dataset_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
if dataset_file:
    df = pd.read_csv(dataset_file)
    st.success("Dataset Loaded Successfully!")
    st.dataframe(df, use_container_width=True)
    athletes = sorted(df["Athlete"].unique())
    events = sorted(df["Event"].unique())
    selected_athlete = st.selectbox("Select Athlete:", athletes)
    athlete_df = df[df["Athlete"] == selected_athlete]
    st.markdown(f"Performance Data for **{selected_athlete}**")
    st.dataframe(athlete_df, use_container_width=True)
    selected_event = st.selectbox("Select Event to Analyze:", athlete_df["Event"].unique())
    event_df = athlete_df[athlete_df["Event"] == selected_event]
    # -------- METRICS --------
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Heart Rate", f"{event_df['HeartRate'].mean():.1f} bpm")
    col2.metric("Avg Speed", f"{event_df['Speed'].mean():.1f} km/h")
    col3.metric("Avg Calories", f"{event_df['Calories'].mean():.1f}")
    # -------- CHARTS --------
    colA, colB = st.columns(2)
    with colA:
        fig1 = px.line(event_df, x="Session", y="HeartRate",
                       title=f"Heart Rate Trend - {selected_event}", markers=True)
        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        fig2 = px.bar(event_df, x="Session", y="Speed",
                      title=f"Speed per Session - {selected_event}",
                      color="Speed", color_continuous_scale="Viridis")
        st.plotly_chart(fig2, use_container_width=True)
    # -------- INJURY REPORT --------
    st.markdown("Injury Report (All Events)")
    injury_count = df["Injury"].value_counts().reset_index()
    injury_count.columns = ["Injury Type", "Count"]
    fig3 = px.pie(injury_count, values="Count", names="Injury Type",
                  title="Overall Injury Distribution")
    st.plotly_chart(fig3, use_container_width=True)
    # -------- SMART INSIGHTS --------
    st.markdown("Smart Insights")
    avg_hr = df["HeartRate"].mean()
    severe_cases = (df["Injury"] == "Severe").sum()
    minor_cases = (df["Injury"] == "Minor").sum()
    if severe_cases > 0:
        st.error("⚠ Severe injuries detected — medical attention required!")
    elif minor_cases > 0:
        st.warning("⚠ Minor injuries noticed — recommend light training.")
    elif avg_hr > 160:
        st.warning("⚠ High average heart rate — possible overtraining.")
    else:
        st.success("✔ Athlete’s overall health looks excellent!")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>Developed by Kanmani Murugaiya</div>",
                unsafe_allow_html=True)
else:
    st.info("Upload your CSV dataset to get started.")

