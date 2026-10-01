import pandas as pd

# Load transition analysis results
df = pd.read_csv("data/transition_analysis.csv")

# Sort transitions by average transition time
bottlenecks = df.sort_values(
    by="mean",
    ascending=False
).reset_index(drop=True)

# Add bottleneck rank
bottlenecks.insert(
    0,
    "Rank",
    range(1, len(bottlenecks) + 1)
)

print("\nCareFlow Bottleneck Analysis")
print("============================")
print(
    bottlenecks[
        ["Rank", "Transition", "count", "mean", "min", "max"]
    ].to_string(index=False)
)

# Save bottleneck results
bottlenecks.to_csv(
    "data/bottleneck_analysis.csv",
    index=False
)

print("\nBottleneck analysis saved to:")
print("data/bottleneck_analysis.csv")