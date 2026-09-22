import pandas as pd

# Load EHR event log
df = pd.read_csv("data/raw/ehr_event_log.csv")

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort data
df = df.sort_values(["Case_ID", "Timestamp"])

# Basic statistics
total_patients = df["Case_ID"].nunique()
total_events = len(df)

# Patient journey duration
journey_duration = df.groupby("Case_ID")["Timestamp"].agg(["min", "max"])

journey_duration["duration_minutes"] = (
    journey_duration["max"] - journey_duration["min"]
).dt.total_seconds() / 60

average_duration = journey_duration["duration_minutes"].mean()
maximum_duration = journey_duration["duration_minutes"].max()
minimum_duration = journey_duration["duration_minutes"].min()

# Activity counts
activity_counts = df["Activity"].value_counts()

# Display results
print("\n===== CAREFLOW PROCESS ANALYSIS =====")

print("\nTotal patients:", total_patients)
print("Total events:", total_events)

print(
    "\nAverage patient journey duration:",
    round(average_duration, 2),
    "minutes"
)

print(
    "Minimum journey duration:",
    round(minimum_duration, 2),
    "minutes"
)

print(
    "Maximum journey duration:",
    round(maximum_duration, 2),
    "minutes"
)

print("\n===== ACTIVITY FREQUENCY =====")
print(activity_counts)

# Save analysis files
journey_duration.to_csv("data/patient_journey_duration.csv")
activity_counts.to_csv("data/activity_counts.csv")

print("\nAnalysis files created successfully!")