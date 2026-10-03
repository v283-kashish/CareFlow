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
loopback_file = BASE_DIR / "data" / "loopback_analysis.csv"

# Load data
ehr_df = pd.read_csv(ehr_file)
duration_df = pd.read_csv(duration_file)
activity_df = pd.read_csv(activity_file)
loopback_df = pd.read_csv(loopback_file)

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
loopback_patients = loopback_df["Loopback"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Patients", total_patients)

with col2:
    st.metric("Total Events", total_events)

with col3:
    st.metric(
        "Avg Journey Duration",
        f"{average_duration:.2f} min"
    )

with col4:
    st.metric("Loopback Patients", loopback_patients)

st.markdown("---")

# Activity frequency
st.subheader("📊 Activity Frequency")

st.bar_chart(
    activity_df.set_index("Activity")["count"]
)

st.markdown("---")

# Loopback Analysis
st.subheader("🔄 Loopback Analysis")

loopback_summary = loopback_df.groupby("Loopback").agg(
    Patients=("Case_ID", "count"),
    Average_Duration=("Duration_Minutes", "mean")
).reset_index()

loopback_summary["Loopback"] = loopback_summary["Loopback"].map({
    True: "With Loopback",
    False: "Without Loopback"
})

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(
        loopback_summary.set_index("Loopback")["Patients"]
    )

with col2:
    st.bar_chart(
        loopback_summary.set_index("Loopback")["Average_Duration"]
    )

st.dataframe(
    loopback_summary,
    use_container_width=True
)

st.markdown("---")

# Bottleneck Analysis
st.subheader("🚨 Process Bottleneck Analysis")

bottleneck_file = BASE_DIR / "data" / "bottleneck_analysis.csv"
bottleneck_df = pd.read_csv(bottleneck_file)

# Display top bottlenecks
st.dataframe(
    bottleneck_df[
        ["Rank", "Transition", "count", "mean", "min", "max"]
    ],
    use_container_width=True
)

# Average transition time chart
st.bar_chart(
    bottleneck_df.set_index("Transition")["mean"]
)

st.markdown("---")

# Transition Analysis
st.subheader("🔄 Patient Transition Analysis")

transition_file = BASE_DIR / "data" / "transition_analysis.csv"
transition_df = pd.read_csv(transition_file)

st.dataframe(
    transition_df[
        ["Transition", "count", "mean", "min", "max"]
    ],
    use_container_width=True
)

st.subheader("⏱️ Average Transition Time")

st.bar_chart(
    transition_df.set_index("Transition")["mean"]
)

st.markdown("---")

# Patient Journey Explorer
st.subheader("🔎 Patient Journey Explorer")

patient_ids = sorted(ehr_df["Case_ID"].unique())

selected_patient = st.selectbox(
    "Select a Patient",
    patient_ids
)

patient_events = ehr_df[
    ehr_df["Case_ID"] == selected_patient
].sort_values("Timestamp")

st.write(f"### Journey for {selected_patient}")

st.dataframe(
    patient_events[
        ["Case_ID", "Activity", "Timestamp"]
    ],
    use_container_width=True
)

st.markdown("---")

# Process Mining Model
st.subheader("🔀 Discovered Patient Process Model")

process_model_file = BASE_DIR / "data" / "process_model.png"

if process_model_file.exists():
    st.image(
        process_model_file,
        caption="Patient Process Model generated using PM4Py",
        use_container_width=True
    )
else:
    st.warning("Process model image not found.")

st.markdown("---")
# Conformance Checking
st.subheader("✅ Conformance Checking")

conformance_file = BASE_DIR / "data" / "conformance_results.csv"
conformance_df = pd.read_csv(conformance_file)

# Conformance summary
conformance_summary = (
    conformance_df["Conformant"]
    .value_counts()
    .rename_axis("Conformance")
    .reset_index(name="Patients")
)

conformance_summary["Conformance"] = conformance_summary[
    "Conformance"
].map({
    True: "Conformant",
    False: "Non-Conformant"
})

col1, col2 = st.columns(2)

with col1:
    conformant_count = (
        conformance_df["Conformant"] == True
    ).sum()

    st.metric(
        "Conformant Patients",
        conformant_count
    )

with col2:
    non_conformant_count = (
        conformance_df["Conformant"] == False
    ).sum()

    st.metric(
        "Non-Conformant Patients",
        non_conformant_count
    )

st.bar_chart(
    conformance_summary.set_index("Conformance")["Patients"]
)

st.dataframe(
    conformance_df[
        ["Case_ID", "Conformant"]
    ],
    use_container_width=True
)

st.markdown("---")

# Patient Journey Duration
st.subheader("⏱️ Patient Journey Duration")

st.dataframe(
    duration_df.sort_values(
        "duration_minutes",
        ascending=False
    ),
    use_container_width=True
)

# Patient Journey Duration Chart
st.subheader("📈 Patient Journey Duration by Patient")

st.bar_chart(
    duration_df.set_index("Case_ID")["duration_minutes"]
)

st.markdown("---")

# Patient Journey Flow
activities = patient_events["Activity"].tolist()

journey_flow = " → ".join(activities)

st.write("### 🔄 Patient Journey Flow")

st.info(journey_flow)

# Loopback status
selected_result = loopback_df[
    loopback_df["Case_ID"] == selected_patient
]

if not selected_result.empty:

    has_loopback = selected_result.iloc[0]["Loopback"]

    if has_loopback:
        st.warning("⚠️ This patient experienced a loopback.")
    else:
        st.success("✅ No loopback detected for this patient.")

    # Selected patient duration
    selected_duration = selected_result["Duration_Minutes"].iloc[0]

    st.metric(
        "Patient Journey Duration",
        f"{selected_duration:.2f} min"
    )

st.markdown("---")

# EHR Event Log
st.subheader("📋 EHR Event Log")

st.dataframe(
    ehr_df,
    use_container_width=True
)
