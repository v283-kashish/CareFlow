import pandas as pd
import pm4py

# 1. Load the EHR event log
df = pd.read_csv("data/raw/ehr_event_log.csv")

# 2. Convert Timestamp into datetime format
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# 3. Sort the events by patient and time
df = df.sort_values(["Case_ID", "Timestamp"])

# 4. Display basic information
print("EHR data loaded successfully!")
print("Total events:", len(df))
print("Total patients:", df["Case_ID"].nunique())

# 5. Convert the CSV into a PM4Py event log
event_log = pm4py.format_dataframe(
    df,
    case_id="Case_ID",
    activity_key="Activity",
    timestamp_key="Timestamp"
)

print("Event log created successfully!")

# 6. Discover the hospital process
net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(
    event_log
)

print("Process model discovered successfully!")

# 7. Save the process model as an image
pm4py.save_vis_petri_net(
    net,
    initial_marking,
    final_marking,
    "data/process_model.png"
)

print("Process model saved to: data/process_model.png")