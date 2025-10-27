# Athletics Dashboard with ML Prediction in Streamlit (Enhanced Visualization)
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import LabelEncoder

# ---------------- Sample Data with More Events ----------------
data = {
    "Athlete": ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah"],
    "Event": ["100m", "200m", "400m", "800m", "3000m", "8000m", "Long Jump", "High Jump"],
    "Speed (m/s)": [9.8, 9.6, 9.3, 8.9, 7.5, 6.8, 8.5, 8.9],
    "Heart Rate (bpm)": [150, 160, 148, 152, 158, 165, 145, 150],
    "Calories": [300, 320, 295, 285, 400, 450, 280, 290],
    "Reaction Time (s)": [0.12, 0.13, 0.14, 0.15, 0.16, 0.18, 0.15, 0.14],
    "Injury Status": ["No", "Yes", "No", "No", "Yes", "No", "No", "Yes"]
}

df = pd.DataFrame(data)

# Encode Injury Status
le = LabelEncoder()
df["Injury Encoded"] = le.fit_transform(df["Injury Status"])  # No=0, Yes=1

# ---------------- ML Models ----------------
X_speed = df[["Heart Rate (bpm)", "Calories", "Reaction Time (s)", "Injury Encoded"]]
y_speed = df["Speed (m/s)"]
speed_model = LinearRegression().fit(X_speed, y_speed)

X_injury = df[["Speed (m/s)", "Heart Rate (bpm)", "Calories", "Reaction Time (s)"]]
y_injury = df["Injury Encoded"]
injury_model = LogisticRegression().fit(X_injury, y_injury)

# ---------------- Streamlit App ----------------
st.set_page_config(page_title="Athletics ML Dashboard", layout="wide")
st.title("🏃‍♂️ Athletics ML Performance Dashboard")

# ---------------- Sidebar: Athlete and Event Selection ----------------
selected_athlete = st.sidebar.selectbox("Select Athlete", df["Athlete"].unique())

# Get selected athlete's events
athlete_events = df[df["Athlete"] == selected_athlete]["Event"].unique()
selected_event = st.sidebar.selectbox("Select Event", athlete_events)

# Filter athlete data for selected event
athlete_data = df[(df["Athlete"] == selected_athlete) & (df["Event"] == selected_event)].iloc[0]

# ---------------- Simulate Athlete Metrics ----------------
st.subheader("Simulate Athlete Metrics")

hr = st.slider("Heart Rate (bpm)", 130, 180, athlete_data["Heart Rate (bpm)"])
cal = st.slider("Calories", 250, 500, athlete_data["Calories"])
rt = st.slider("Reaction Time (s)", 0.10, 0.20, athlete_data["Reaction Time (s)"], 0.01)
injury = st.radio("Injury Status", options=["No","Yes"], index=0 if athlete_data["Injury Status"]=="No" else 1)
injury_val = 0 if injury=="No" else 1

# ---------------- ML Prediction ----------------
pred_speed = speed_model.predict([[hr, cal, rt, injury_val]])[0]
pred_injury_prob = injury_model.predict_proba([[pred_speed, hr, cal, rt]])[0][1]
pred_injury = "Yes" if pred_injury_prob >= 0.5 else "No"

st.markdown(f"**Predicted Speed:** {pred_speed:.2f} m/s | **Predicted Injury Risk:** {pred_injury}")

# ---------------- Filter Data for Selected Athlete and Event ----------------
filtered_df = df[(df["Athlete"] == selected_athlete) & (df["Event"] == selected_event)]

# ---------------- Enhanced Plots ----------------
st.subheader("Performance Graphs")

# Speed Comparison
speed_fig = px.bar(
    filtered_df, x="Athlete", y="Speed (m/s)", color="Event", 
    barmode="group", title="🏎️ Speed Comparison",
    template="plotly_dark", text="Speed (m/s)", height=400
)
speed_fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
speed_fig.update_layout(yaxis=dict(title="Speed (m/s)", range=[0, max(filtered_df["Speed (m/s)"])+2]))
st.plotly_chart(speed_fig, use_container_width=True)

# Heart Rate
heart_fig = px.line(
    filtered_df, x="Athlete", y="Heart Rate (bpm)", color="Event", markers=True,
    title="❤️ Heart Rate", template="plotly_dark", height=400
)
heart_fig.update_traces(mode="lines+markers+text", text=filtered_df["Heart Rate (bpm)"])
heart_fig.update_layout(yaxis=dict(title="Heart Rate (bpm)"))
st.plotly_chart(heart_fig, use_container_width=True)

# Calories Burned
calories_fig = px.bar(
    filtered_df, x="Calories", y="Athlete", color="Event", orientation="h",
    barmode="group", title="🔥 Calories Burned", template="plotly_dark", height=400
)
calories_fig.update_layout(xaxis=dict(title="Calories"), yaxis=dict(title="Athlete"))
st.plotly_chart(calories_fig, use_container_width=True)

# Reaction Time vs Speed
reaction_fig = px.scatter(
    filtered_df, x="Athlete", y="Reaction Time (s)", color="Event",
    size="Speed (m/s)", hover_data=["Heart Rate (bpm)", "Calories"], 
    title="⚡ Reaction Time vs Speed", template="plotly_dark", height=400
)
reaction_fig.update_layout(yaxis=dict(title="Reaction Time (s)"))
st.plotly_chart(reaction_fig, use_container_width=True)

# ---------------- Data Table ----------------
st.subheader("Athlete Details")
st.dataframe(filtered_df)
