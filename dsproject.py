import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import LabelEncoder
import numpy as np

# ===============================
# 🎨 PAGE CONFIGURATION
# ===============================
st.set_page_config(
    page_title="🏃 Athletics ML Dashboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# 🏅 HEADER SECTION
# ===============================
st.markdown(
    """
    <style>
    .big-title {
        text-align: center;
        color: #FF4B4B;
        font-size: 45px;
        font-weight: bold;
        margin-bottom: -10px;
    }
    .sub-title {
        text-align: center;
        color: gray;
        font-size: 18px;
        margin-bottom: 20px;
    }
    </style>
    <h1 class='big-title'>🏃‍♀️ Athletics ML Performance Dashboard</h1>
    <p class='sub-title'>Analyze athlete data, predict performance, and visualize insights</p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ===============================
# 📂 DATA UPLOAD SECTION
# ===============================
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File Uploaded Successfully!")
    st.write("### 📋 Dataset Preview")
    st.dataframe(df.head())

    # ===============================
    # 🔍 BASIC STATS
    # ===============================
    st.markdown("### 📈 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # ===============================
    # 🧠 MODEL TRAINING SECTION
    # ===============================
    st.sidebar.divider()
    st.sidebar.header("⚙️ ML Prediction Setup")

    target_col = st.sidebar.selectbox("🎯 Select Target Column", df.columns)
    feature_cols = st.sidebar.multiselect("📊 Select Feature Columns", [c for c in df.columns if c != target_col])

    if feature_cols and target_col:
        X = df[feature_cols]
        y = df[target_col]

        # Encode categorical variables
        for col in X.select_dtypes(include=["object"]).columns:
            X[col] = LabelEncoder().fit_transform(X[col])

        if y.dtype == "object":
            model = LogisticRegression()
        else:
            model = LinearRegression()

        model.fit(X, y)
        st.sidebar.success("✅ Model Trained Successfully!")

        # ===============================
        # 🔢 PREDICTION SECTION
        # ===============================
        st.markdown("### 🔢 Predict Athlete Performance")
        input_data = {}
        for col in feature_cols:
            val = st.number_input(f"Enter value for {col}", float(X[col].min()), float(X[col].max()))
            input_data[col] = val

        if st.button("🚀 Predict"):
            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]
            st.success(f"🏅 Predicted Output: **{prediction:.2f}**")

        # ===============================
        # 📊 VISUALIZATION SECTION
        # ===============================
        st.divider()
        st.markdown("### 📊 Visualization Dashboard")

        chart_type = st.selectbox("Select Chart Type", ["Scatter", "Bar", "Line", "Histogram"])
        x_col = st.selectbox("X-axis", df.columns)
        y_col = st.selectbox("Y-axis", df.columns)

        if chart_type == "Scatter":
            fig = px.scatter(df, x=x_col, y=y_col, color=target_col, title="Scatter Plot")
        elif chart_type == "Bar":
            fig = px.bar(df, x=x_col, y=y_col, color=target_col, title="Bar Chart")
        elif chart_type == "Line":
            fig = px.line(df, x=x_col, y=y_col, color=target_col, title="Line Chart")
        else:
            fig = px.histogram(df, x=x_col, color=target_col, title="Histogram")

        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Please upload a CSV file to begin analysis.")

# ===============================
# 🦶 FOOTER
# ===============================
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>Made with ❤️ by Kanmani Murugaiya | Powered by Streamlit</p>",
    unsafe_allow_html=True
)
