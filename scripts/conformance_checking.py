import pandas as pd

# Load EHR event log
df = pd.read_csv("data/raw/ehr_event_log.csv")

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort events correctly
df = df.sort_values(["Case_ID", "Timestamp"])

# Expected patient journey
expected_process = [
    "Registration",
    "Triage",
    "Doctor Consultation",
    "X-Ray",
    "Billing",
    "Discharge"
]

results = []

# Check each patient's actual journey
for case_id, patient_df in df.groupby("Case_ID"):

    actual_process = patient_df["Activity"].tolist()

    # Compare actual journey with expected journey
    is_conformant = actual_process == expected_process

    results.append({
        "Case_ID": case_id,
        "Expected_Process": " → ".join(expected_process),
        "Actual_Process": " → ".join(actual_process),
        "Conformant": is_conformant
    })

# Create result dataframe
result_df = pd.DataFrame(results)

# Display results
print("\nConformance Checking Results:\n")
print(result_df[["Case_ID", "Conformant"]])

# Summary
summary = result_df["Conformant"].value_counts()

print("\nConformance Summary:\n")
print(summary)

# Save results
result_df.to_csv(
    "data/conformance_results.csv",
    index=False
)

print("\nConformance results saved to data/conformance_results.csv")