# modern_streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 🧭 Page Configuration
st.set_page_config(page_title="Athlete Dashboard", layout="wide", page_icon="🏃‍♀️")

# 🌈 Stylish Header
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(135deg, #e0f7fa 0%, #ffffff 100%);
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
            color: #555;
        }
        .footer {
            text-align: center;
            color: #0077b6;
            margin-top: 30px;
            font-size: 14px;
        }
    </style>

    <div class="main">
        <h1>🏃‍♀️ Athlete Performance Dashboard</h1>
        <p>Auto Dataset Generator + Visual Analytics</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 🧍‍♀️ Athlete Name Input
athlete_name = st.text_input("Enter Athlete Name:", placeholder="e.g., Kanmani")

if athlete_name:
    st.success(f"Generating performance data for **{athlete_name}** 🏅")

    # 🧮 Auto-generate random dataset
    np.random.seed(42)
    data = {
        "Session": range(1, 11),
        "HeartRate": np.random.randint(60, 180, 10),
        "Speed": np.round(np.random.uniform(5, 25, 10), 2),
        "Calories": np.random.randint(200, 800, 10),
        "ReactionTime": np.round(np.random.uniform(0.2, 1.0, 10), 2)
    }
    df = pd.DataFrame(data)
    df["Athlete"] = athlete_name

    # 🧾 Show dataset
    st.markdown("### 📋 Generated Dataset")
    st.dataframe(df, use_container_width=True)

    # 📊 Summary stats
    st.markdown("### 📊 Quick Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("❤️ Avg Heart Rate", f"{df['HeartRate'].mean():.1f} bpm")
    col2.metric("⚡ Avg Speed", f"{df['Speed'].mean():.1f} km/h")
    col3.metric("🔥 Avg Calories", f"{df['Calories'].mean():.1f}")

    # 📈 Charts Section
    st.markdown("### 📉 Performance Trends")

    colA, colB = st.columns(2)

    with colA:
        fig1 = px.line(df, x="Session", y="HeartRate", title="Heart Rate per Session", markers=True, color_discrete_sequence=["#0077b6"])
        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        fig2 = px.bar(df, x="Session", y="Speed", title="Speed per Session", color="Speed", color_continuous_scale="Blues")
        st.plotly_chart(fig2, use_container_width=True)

    # 🧠 Extra insight
    st.markdown("### 🧠 Insights")
    if df["HeartRate"].mean() > 150:
        st.warning("⚠️ High average heart rate — athlete might be overtraining.")
    else:
        st.info("✅ Heart rate levels look balanced and healthy!")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>💙 Developed by Kanmani Murugaiya | Streamlit Cloud App</div>", unsafe_allow_html=True)

else:
    st.info("👆 Please enter an athlete name to auto-generate performance data.")
