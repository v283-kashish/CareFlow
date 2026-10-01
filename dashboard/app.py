import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="CareFlow Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

ehr_file = BASE_DIR / "data" / "raw" / "ehr_event_log.csv"
duration_file = BASE_DIR / "data" / "patient_journey_duration.csv"
activity_file = BASE_DIR / "data" / "activity_counts.csv"

# Load data
ehr_df = pd.read_csv(ehr_file)
duration_df = pd.read_csv(duration_file)
activity_df = pd.read_csv(activity_file)

# Convert timestamp
ehr_df["Timestamp"] = pd.to_datetime(ehr_df["Timestamp"])

# Title
st.title("🏥 CareFlow")
st.subheader("Healthcare Patient Journey & Process Mining Dashboard")

st.markdown("---")

# Key metrics
total_patients = ehr_df["Case_ID"].nunique()
total_events = len(ehr_df)
average_duration = duration_df["duration_minutes"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Patients", total_patients)

with col2:
    st.metric("Total Events", total_events)

with col3:
    st.metric("Avg Journey Duration", f"{average_duration:.2f} min")

st.markdown("---")

# Activity frequency
st.subheader("📊 Activity Frequency")

st.bar_chart(
    activity_df.set_index("Activity")["count"]
)

# Patient journey duration
st.subheader("⏱️ Patient Journey Duration")

st.dataframe(
    duration_df.sort_values(
        "duration_minutes",
        ascending=False
    ),
    use_container_width=True
)

# Raw event data
st.subheader("📋 EHR Event Log")

st.dataframe(
    ehr_df,
    use_container_width=True
)