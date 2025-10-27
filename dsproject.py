import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

# 🌐 Page Config
st.set_page_config(page_title="Athlete Multi-Event Dashboard", layout="wide", page_icon="🏃‍♂️")

# 🎨 Custom CSS
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
    p {
        text-align: center;
        color: #333;
    }
    .footer {
        text-align: center;
        color: #0077b6;
        margin-top: 30px;
        font-size: 14px;
    }
</style>

<div class="main">
    <h1>🏅 Multi-Event Athlete Performance Dashboard</h1>
    <p>Auto Dataset Generator + Injury Tracker + Event Comparison</p>
</div>
""", unsafe_allow_html=True)

# 🧍 Athlete List
athletes = [
    "Kanmani", "Priya", "Arjun", "Rahul", "Sneha", "Vishal", "Kavin", "Nisha", "Deepak", "Lavanya",
    "Harini", "Santhosh", "Meena", "Ravi", "Swetha", "Dinesh", "Aarthi", "Vikram", "Gokul", "Divya",
    "Karthik", "Sanjana", "Bala", "Naveen", "Preethi"
]

# 🏃 Event List
events = [
    "100m Sprint", "200m Sprint", "400m Sprint", "800m Run", "Long Jump", "High Jump",
    "Shot Put", "Javelin Throw", "Discus Throw", "Marathon", "Relay 4x100m",
    "Pole Vault", "Triple Jump", "Hammer Throw", "Steeplechase"
]

# 🧍 Athlete Selection
selected_athlete = st.selectbox("Select Athlete:", athletes)

# 📊 Number of Events
selected_events = st.multiselect("Select Events (or leave empty for random):", events, default=random.sample(events, 3))

if selected_athlete:
    st.success(f"Generating event performance data for **{selected_athlete}** 🏃‍♀️")

    # 🎲 Data Generation
    np.random.seed(random.randint(1, 1000))
    injuries = ["No Injury", "Minor", "Moderate", "Severe"]
    all_data = []

    if not selected_events:
        selected_events = random.sample(events, 5)

    for event in selected_events:
        for session in range(1, 6):  # 5 sessions per event
            all_data.append({
                "Athlete": selected_athlete,
                "Event": event,
                "Session": session,
                "HeartRate": np.random.randint(60, 190),
                "Speed": np.round(np.random.uniform(5, 28), 2),
                "Calories": np.random.randint(250, 900),
                "ReactionTime": np.round(np.random.uniform(0.2, 1.2), 2),
                "Injury": random.choice(injuries)
            })

    df = pd.DataFrame(all_data)

    # 🧾 Display Dataset
    st.markdown("### 📋 Generated Multi-Event Dataset")
    st.dataframe(df, use_container_width=True)

    # 📈 Event-Wise Analysis
    st.markdown("### 📈 Event-Wise Performance Overview")
    selected_event = st.selectbox("Select an Event to Analyze:", sorted(df["Event"].unique()))

    event_df = df[df["Event"] == selected_event]

    col1, col2, col3 = st.columns(3)
    col1.metric("❤️ Avg Heart Rate", f"{event_df['HeartRate'].mean():.1f} bpm")
    col2.metric("⚡ Avg Speed", f"{event_df['Speed'].mean():.1f} km/h")
    col3.metric("🔥 Avg Calories", f"{event_df['Calories'].mean():.1f}")

    # 📊 Charts
    colA, colB = st.columns(2)
    with colA:
        fig1 = px.line(event_df, x="Session", y="HeartRate", title=f"Heart Rate Trend - {selected_event}", markers=True)
        st.plotly_chart(fig1, use_container_width=True)
    with colB:
        fig2 = px.bar(event_df, x="Session", y="Speed", title=f"Speed per Session - {selected_event}", color="Speed", color_continuous_scale="Viridis")
        st.plotly_chart(fig2, use_container_width=True)

    # 💉 Injury Chart
    st.markdown("### 💉 Injury Report (All Events)")
    injury_summary = df["Injury"].value_counts().reset_index()
    injury_summary.columns = ["Injury Type", "Count"]
    fig3 = px.pie(injury_summary, values="Count", names="Injury Type", title="Overall Injury Distribution", color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig3, use_container_width=True)

    # 🧠 Insights
    st.markdown("### 🧠 Smart Insights")
    avg_hr = df["HeartRate"].mean()
    severe_cases = (df["Injury"] == "Severe").sum()
    minor_cases = (df["Injury"] == "Minor").sum()

    if severe_cases > 0:
        st.error("🚑 Severe injuries detected — immediate rest and medical attention required!")
    elif minor_cases > 0:
        st.warning("💤 Minor injuries noticed — suggest light training for recovery.")
    elif avg_hr > 160:
        st.warning("⚠️ High average heart rate — possible overtraining detected.")
    else:
        st.success("✅ Athlete’s health and performance are excellent!")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>💚 Developed by Kanmani Murugaiya | Streamlit Multi-Event Dashboard</div>", unsafe_allow_html=True)

else:
    st.info("👆 Select an athlete name to generate performance data.")
