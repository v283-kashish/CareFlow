import pandas as pd

# Load EHR event data
df = pd.read_csv("data/raw/ehr_event_log.csv")

# Convert Timestamp to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort events for each patient
df = df.sort_values(["Case_ID", "Timestamp"])

# Check whether a patient has a loopback
# A loopback is identified when an activity occurs again
loopback_results = []

for case_id, patient_df in df.groupby("Case_ID"):
    activities = patient_df["Activity"].tolist()

    has_loopback = len(activities) != len(set(activities))

    # Calculate total journey duration
    duration = (
        patient_df["Timestamp"].max()
        - patient_df["Timestamp"].min()
    ).total_seconds() / 60

    loopback_results.append({
        "Case_ID": case_id,
        "Loopback": has_loopback,
        "Duration_Minutes": duration
    })

# Create result DataFrame
result_df = pd.DataFrame(loopback_results)

# Display summary
summary = result_df.groupby("Loopback")["Duration_Minutes"].agg(
    ["count", "mean", "min", "max"]
)

print("\nLoopback Analysis")
print("=================")
print(summary)

# Save detailed results
result_df.to_csv(
    "data/loopback_analysis.csv",
    index=False
)

print("\nDetailed results saved to:")
print("data/loopback_analysis.csv")