import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="FloodShield AI",
    page_icon="🌊",
    layout="wide"
)

# Load files
df = pd.read_csv("flood_data.csv")

with open("flood_model.pkl", "rb") as file:
    model = pickle.load(file)

# ---------------- HEADER ----------------

st.title("🌊 FloodShield AI")
st.subheader("Flash Flood Prediction & Early Warning System")

st.write(
    "AI-based prototype for identifying flood-risk areas "
    "and providing early warnings."
)

st.divider()

# ---------------- PREDICT ALL AREAS ----------------

features = [
    "Rainfall",
    "Soil_moisture",
    "Slope",
    "Water_Level"
]

df["AI_Risk"] = model.predict(df[features])
df["AI_Risk"] = df["AI_Risk"].astype(str).str.lower()

# ---------------- DASHBOARD SUMMARY ----------------

st.header("🚨 Flood Risk Dashboard")

critical = df[df["AI_Risk"] == "critical"]
high = df[df["AI_Risk"] == "high"]
moderate = df[df["AI_Risk"] == "moderate"]
low = df[df["AI_Risk"] == "low"]

c1, c2, c3, c4 = st.columns(4)

c1.metric("🔴 Critical Areas", len(critical))
c2.metric("🟠 High Risk Areas", len(high))
c3.metric("🟡 Moderate Areas", len(moderate))
c4.metric("🟢 Low Risk Areas", len(low))

st.divider()

# ---------------- ALERT ----------------

if len(critical) > 0 or len(high) > 0:
    st.error(
        "🚨 FLOOD WARNING: High-risk areas detected. "
        "People in affected areas should move to a safe location "
        "and follow local emergency instructions."
    )

# ---------------- RISKY AREAS ----------------

st.header("🔴 Risky Areas")

risky = df[df["AI_Risk"].isin(["critical", "high", "moderate"])]

if len(risky) > 0:
    risky_display = risky[
        ["Area", "Location", "Rainfall", "Soil_moisture",
         "Slope", "Water_Level", "AI_Risk"]
    ]

    st.dataframe(
        risky_display,
        width="stretch",
        hide_index=True
    )
else:
    st.success("✅ No risky areas detected.")

# ---------------- SAFE AREAS ----------------

st.header("🟢 Low-Risk / Safer Areas")

safe = df[df["AI_Risk"] == "low"]

if len(safe) > 0:
    safe_display = safe[
        ["Area", "Location", "Rainfall", "Soil_moisture",
         "Slope", "Water_Level", "AI_Risk"]
    ]

    st.dataframe(
        safe_display,
        width="stretch",
        hide_index=True
    )
else:
    st.info("No low-risk areas found.")

st.divider()

# ---------------- PARTICULAR AREA ----------------

st.header("📍 Check Particular Area")

selected_area = st.selectbox(
    "Select an area",
    df["Area"].dropna().unique()
)

area_data = df[df["Area"] == selected_area].iloc[0]

st.subheader(f"📍 {selected_area}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌧️ Rainfall", f"{area_data['Rainfall']} mm")
col2.metric("💧 Soil Moisture", f"{area_data['Soil_moisture']} %")
col3.metric("⛰️ Slope", f"{area_data['Slope']}°")
col4.metric("🌊 Water Level", f"{area_data['Water_Level']} m")

risk = area_data["AI_Risk"]

st.subheader("🚨 Area Risk Result")

if risk == "critical":
    st.error("🔴 CRITICAL RISK")
    st.error(
        "🚨 IMMEDIATE WARNING: This area has very high flood risk. "
        "Move to a safer location and follow official emergency instructions."
    )

elif risk == "high":
    st.warning("🟠 HIGH RISK")
    st.warning(
        "⚠️ FLOOD ALERT: Avoid staying in this area if authorities "
        "issue an evacuation warning."
    )

elif risk == "moderate":
    st.warning("🟡 MODERATE RISK")
    st.info(
        "⚠️ Monitor rainfall and water levels. "
        "Stay alert for further warnings."
    )

else:
    st.success("🟢 LOW RISK")
    st.success("✅ No significant flood risk detected in this prototype.")

st.write(f"### Predicted Risk: {risk.upper()}")

# ---------------- WHY RISK ----------------

st.subheader("🔎 Why is this area at risk?")

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

# ---------------- COMPLETE DATA ----------------

st.header("📊 Complete Area Risk Data")

st.dataframe(
    df[
        [
            "Area",
            "Location",
            "Rainfall",
            "Soil_moisture",
            "Slope",
            "Water_Level",
            "Historical_Risk",
            "Risk_Label",
            "AI_Risk"
        ]
    ],
    width="stretch",
    height=500,
    hide_index=True
)

st.divider()

st.caption(
    "FloodShield AI — SIH Prototype | "
    "Demonstration purposes only."
)