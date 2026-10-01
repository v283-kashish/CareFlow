import pandas as pd

# Load EHR event data
df = pd.read_csv("data/raw/ehr_event_log.csv")

# Convert timestamp to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort patient events
df = df.sort_values(["Case_ID", "Timestamp"])

# Get the previous activity and timestamp for each patient
df["Previous_Activity"] = df.groupby("Case_ID")["Activity"].shift(1)
df["Previous_Timestamp"] = df.groupby("Case_ID")["Timestamp"].shift(1)

# Calculate transition time in minutes
df["Transition_Time_Minutes"] = (
    df["Timestamp"] - df["Previous_Timestamp"]
).dt.total_seconds() / 60

# Remove first event of every patient
transitions = df.dropna(
    subset=["Previous_Activity", "Transition_Time_Minutes"]
).copy()

# Create transition name
transitions["Transition"] = (
    transitions["Previous_Activity"]
    + " → "
    + transitions["Activity"]
)

# Calculate statistics for each transition
summary = transitions.groupby("Transition")[
    "Transition_Time_Minutes"
].agg(
    ["count", "mean", "min", "max"]
).reset_index()

# Round values
summary[["mean", "min", "max"]] = summary[
    ["mean", "min", "max"]
].round(2)

# Display results
print("\nTransition Analysis")
print("===================")
print(summary.to_string(index=False))

# Save results
summary.to_csv(
    "data/transition_analysis.csv",
    index=False
)

print("\nTransition analysis saved to:")
print("data/transition_analysis.csv")