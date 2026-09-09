import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="FloodShield AI",
    page_icon="🌊",
    layout="wide"
)

# Load trained model
with open("flood_model.pkl", "rb") as file:
    model = pickle.load(file)

st.title("🌊 FloodShield AI")
st.subheader("Flash Flood Prediction & Early Warning System")

st.write(
    "AI-based prototype for assessing flood risk using "
    "rainfall, soil moisture, slope and water-level data."
)

st.divider()

st.header("📊 Enter Environmental Data")

col1, col2 = st.columns(2)

with col1:
    rainfall = st.number_input(
        "🌧️ Rainfall (mm)",
        min_value=0.0,
        max_value=1000.0,
        value=100.0
    )

    soil_moisture = st.number_input(
        "💧 Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0
    )

with col2:
    slope = st.number_input(
        "⛰️ Slope (°)",
        min_value=0.0,
        max_value=90.0,
        value=25.0
    )

    water_level = st.number_input(
        "🌊 Water Level (m)",
        min_value=0.0,
        max_value=20.0,
        value=3.0
    )

st.divider()

if st.button("🔍 Predict Flood Risk", use_container_width=True):

    input_data = pd.DataFrame(
        [[rainfall, soil_moisture, slope, water_level]],
        columns=[
            "Rainfall",
            "Soil_moisture",
            "Slope",
            "Water_Level"
        ]
    )

    prediction = model.predict(input_data)[0]
    prediction = str(prediction).lower()

    st.header("🚨 Flood Risk Result")

    if prediction == "critical":
        st.error("🔴 CRITICAL FLOOD RISK")
    elif prediction == "high":
        st.warning("🟠 HIGH FLOOD RISK")
    elif prediction == "moderate":
        st.warning("🟡 MODERATE FLOOD RISK")
    else:
        st.success("🟢 LOW FLOOD RISK")

    st.write("### Predicted Risk Level")
    st.write(f"## {prediction.upper()}")

    st.write("### 📋 Environmental Parameters")

    result = pd.DataFrame({
        "Parameter": [
            "Rainfall",
            "Soil Moisture",
            "Slope",
            "Water Level"
        ],
        "Value": [
            f"{rainfall} mm",
            f"{soil_moisture} %",
            f"{slope}°",
            f"{water_level} m"
        ]
    })

    st.table(result)

st.divider()

st.caption(
    "FloodShield AI — SIH Prototype | "
    "For demonstration purposes only."
)