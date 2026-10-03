import pandas as pd

# Load analysis results
bottleneck_df = pd.read_csv(
    "data/bottleneck_analysis.csv"
)

loopback_df = pd.read_csv(
    "data/loopback_analysis.csv"
)

transition_df = pd.read_csv(
    "data/transition_analysis.csv"
)

recommendations = []

# --------------------------------------------------
# 1. Bottleneck-based recommendation
# --------------------------------------------------

top_bottleneck = bottleneck_df.iloc[0]

recommendations.append({
    "Issue": "Highest Average Transition Time",
    "Finding": (
        f"{top_bottleneck['Transition']} has the "
        f"highest average transition time of "
        f"{top_bottleneck['mean']:.2f} minutes."
    ),
    "Recommendation": (
        "Review this transition for unnecessary waiting, "
        "manual processing, or resource constraints."
    )
})

# --------------------------------------------------
# 2. Loopback-based recommendation
# --------------------------------------------------

loopback_count = (
    loopback_df["Loopback"] == True
).sum()

total_patients = loopback_df["Case_ID"].nunique()

loopback_percentage = (
    loopback_count / total_patients
) * 100

recommendations.append({
    "Issue": "Patient Loopbacks",
    "Finding": (
        f"{loopback_count} out of {total_patients} "
        f"patients ({loopback_percentage:.1f}%) "
        "experienced a loopback."
    ),
    "Recommendation": (
        "Investigate the reason for patients returning "
        "to an earlier activity and improve information "
        "availability or process coordination."
    )
})

# --------------------------------------------------
# 3. X-Ray transition recommendation
# --------------------------------------------------

xray_triage = transition_df[
    transition_df["Transition"] == "X-Ray → Triage"
]

if not xray_triage.empty:

    xray_mean = xray_triage["mean"].iloc[0]

    recommendations.append({
        "Issue": "X-Ray to Triage Loopback",
        "Finding": (
            f"X-Ray → Triage occurs with an average "
            f"transition time of {xray_mean:.2f} minutes."
        ),
        "Recommendation": (
            "Review the information or documentation "
            "required after X-Ray before sending patients "
            "back to Triage."
        )
    })

# --------------------------------------------------
# 4. Process standardization recommendation
# --------------------------------------------------

recommendations.append({
    "Issue": "Process Standardization",
    "Finding": (
        "Some patient journeys do not follow the "
        "expected process sequence."
    ),
    "Recommendation": (
        "Define clear process checkpoints between "
        "Registration, Triage, Consultation, X-Ray, "
        "Billing, and Discharge."
    )
})

# Create recommendation dataframe
recommendation_df = pd.DataFrame(
    recommendations
)

# Display recommendations
print("\nProcess Improvement Recommendations:\n")

print(
    recommendation_df.to_string(index=False)
)

# Save recommendations
recommendation_df.to_csv(
    "data/process_recommendations.csv",
    index=False
)

print(
    "\nRecommendations saved to "
    "data/process_recommendations.csv"
)