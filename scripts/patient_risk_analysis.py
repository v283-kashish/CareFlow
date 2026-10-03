import pandas as pd

# Load patient journey duration data
duration_df = pd.read_csv(
    "data/patient_journey_duration.csv"
)

# Load loopback analysis
loopback_df = pd.read_csv(
    "data/loopback_analysis.csv"
)

# Load conformance results
conformance_df = pd.read_csv(
    "data/conformance_results.csv"
)

# Combine all patient-level information
risk_df = duration_df.merge(
    loopback_df[
        ["Case_ID", "Loopback"]
    ],
    on="Case_ID"
)

risk_df = risk_df.merge(
    conformance_df[
        ["Case_ID", "Conformant"]
    ],
    on="Case_ID"
)

# Calculate average journey duration
average_duration = risk_df["duration_minutes"].mean()

# Calculate risk score
risk_df["Risk_Score"] = 0

# Add risk points for long journeys
risk_df.loc[
    risk_df["duration_minutes"] > average_duration,
    "Risk_Score"
] += 1

# Add risk points for loopbacks
risk_df.loc[
    risk_df["Loopback"] == True,
    "Risk_Score"
] += 1

# Add risk points for non-conformance
risk_df.loc[
    risk_df["Conformant"] == False,
    "Risk_Score"
] += 1

# Convert risk score into risk level
def assign_risk_level(score):

    if score == 0:
        return "Low"

    elif score == 1:
        return "Medium"

    else:
        return "High"


risk_df["Risk_Level"] = risk_df[
    "Risk_Score"
].apply(assign_risk_level)

# Display results
print("\nPatient Risk / Delay Analysis:\n")

print(
    risk_df[
        [
            "Case_ID",
            "duration_minutes",
            "Loopback",
            "Conformant",
            "Risk_Score",
            "Risk_Level"
        ]
    ]
)

# Display risk summary
print("\nRisk Level Summary:\n")

print(
    risk_df["Risk_Level"].value_counts()
)

# Save results
risk_df.to_csv(
    "data/patient_risk_analysis.csv",
    index=False
)

print(
    "\nPatient risk analysis saved to "
    "data/patient_risk_analysis.csv"
)