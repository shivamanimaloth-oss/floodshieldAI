import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="FloodShield AI",
    page_icon="🌊",
    layout="wide"
)

# Load data
df = pd.read_csv("flood_data.csv")

# Load ML model
with open("flood_model.pkl", "rb") as file:
    model = pickle.load(file)

st.title("🌊 FloodShield AI")
st.subheader("Flash Flood Prediction & Early Warning System")

st.write(
    "AI-based prototype for identifying flood-risk areas "
    "and generating early warning alerts."
)

st.divider()

# =====================================================
# RISK PREDICTION FOR PARTICULAR AREA
# =====================================================

st.header("📍 Check Particular Area Risk")

area_column = "Area" if "Area" in df.columns else "Location"

areas = df[area_column].dropna().unique()

selected_area = st.selectbox(
    "Select Area",
    areas
)

area_data = df[df[area_column] == selected_area].iloc[0]

# Input data for ML model
input_data = pd.DataFrame(
    [[
        area_data["Rainfall"],
        area_data["Soil_moisture"],
        area_data["Slope"],
        area_data["Water_Level"]
    ]],
    columns=[
        "Rainfall",
        "Soil_moisture",
        "Slope",
        "Water_Level"
    ]
)

prediction = str(model.predict(input_data)[0]).lower()

# =====================================================
# AREA DETAILS
# =====================================================

st.subheader(f"📍 {selected_area}")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🌧️ Rainfall",
    f"{area_data['Rainfall']} mm"
)

c2.metric(
    "💧 Soil Moisture",
    f"{area_data['Soil_moisture']} %"
)

c3.metric(
    "⛰️ Slope",
    f"{area_data['Slope']}°"
)

c4.metric(
    "🌊 Water Level",
    f"{area_data['Water_Level']} m"
)

st.divider()

# =====================================================
# RISK RESULT
# =====================================================

st.header("🚨 Flood Risk Result")

if prediction == "critical":

    st.error(
        "🔴 CRITICAL FLOOD RISK\n\n"
        "⚠️ IMMEDIATE ALERT: Move to a safer location "
        "and follow local emergency instructions."
    )

elif prediction == "high":

    st.error(
        "🟠 HIGH FLOOD RISK\n\n"
        "⚠️ ALERT: Avoid low-lying areas and prepare "
        "to move to a safer location."
    )

elif prediction == "moderate":

    st.warning(
        "🟡 MODERATE FLOOD RISK\n\n"
        "⚠️ Stay alert and monitor weather conditions."
    )

else:

    st.success(
        "🟢 LOW FLOOD RISK\n\n"
        "✅ No immediate high-risk condition detected."
    )

st.write(
    f"### Predicted Risk Level: **{prediction.upper()}**"
)

st.divider()

# =====================================================
# WHY IS THIS AREA RISKY?
# =====================================================

st.header("🔎 Why is this area risky?")

reasons = []

if area_data["Rainfall"] > 100:
    reasons.append("🌧️ High rainfall")

if area_data["Soil_moisture"] > 70:
    reasons.append("💧 High soil moisture")

if area_data["Slope"] > 30:
    reasons.append("⛰️ High slope")

if area_data["Water_Level"] > 4:
    reasons.append("🌊 High water level")

if reasons:

    for reason in reasons:
        st.write("•", reason)

else:

    st.write("✅ No major risk factors detected.")

st.divider()

# =====================================================
# ALL RISKY AREAS
# =====================================================

st.header("🔴 Risky Areas")

risky_rows = []

for _, row in df.iterrows():

    test_input = pd.DataFrame(
        [[
            row["Rainfall"],
            row["Soil_moisture"],
            row["Slope"],
            row["Water_Level"]
        ]],
        columns=[
            "Rainfall",
            "Soil_moisture",
            "Slope",
            "Water_Level"
        ]
    )

    risk = str(model.predict(test_input)[0]).lower()

    if risk in ["high", "critical"]:

        risky_rows.append({
            "Area": row[area_column],
            "Rainfall": row["Rainfall"],
            "Soil Moisture": row["Soil_moisture"],
            "Slope": row["Slope"],
            "Water Level": row["Water_Level"],
            "Risk Level": risk.upper()
        })

if risky_rows:

    risky_df = pd.DataFrame(risky_rows)

    st.dataframe(
        risky_df,
        width="stretch",
        hide_index=True
    )

    st.error(
        f"🚨 ALERT: {len(risky_df)} risky area(s) detected. "
        "Residents in high-risk locations should follow "
        "official local emergency guidance."
    )

else:

    st.success("✅ No High/Critical risk areas detected.")

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "FloodShield AI — SIH Prototype | "
    "For demonstration purposes only."
)