import csv
import random
from datetime import datetime, timedelta


# Number of patients we want to generate
NUMBER_OF_PATIENTS = 100


# Activities in a normal patient journey
NORMAL_PROCESS = [
    "Registration",
    "Triage",
    "Doctor Consultation",
    "X-Ray",
    "Billing",
    "Discharge"
]


def generate_patient_events(case_id):
    """
    Generate the event sequence for one patient.
    """

    events = []

    # Starting time for this patient's hospital visit
    current_time = datetime.now().replace(microsecond=0)

    # Decide whether this patient will have a loop-back
    has_loopback = random.random() < 0.30

    for activity in NORMAL_PROCESS:

        events.append({
            "Case_ID": case_id,
            "Activity": activity,
            "Timestamp": current_time
        })

        # Add random waiting time between activities
        waiting_minutes = random.randint(5, 30)
        current_time += timedelta(minutes=waiting_minutes)

        # Create a loop-back after X-Ray
        if activity == "X-Ray" and has_loopback:

            events.append({
                "Case_ID": case_id,
                "Activity": "Triage",
                "Timestamp": current_time
            })

            current_time += timedelta(minutes=random.randint(5, 20))

            events.append({
                "Case_ID": case_id,
                "Activity": "Doctor Consultation",
                "Timestamp": current_time
            })

            current_time += timedelta(minutes=random.randint(5, 20))

    return events


def generate_dataset():
    """
    Generate event logs for all patients.
    """

    all_events = []

    for patient_number in range(1, NUMBER_OF_PATIENTS + 1):

        case_id = f"P{patient_number:04d}"

        patient_events = generate_patient_events(case_id)

        all_events.extend(patient_events)

    return all_events


def save_to_csv(events):

    output_file = "data/raw/ehr_event_log.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as file:

        fieldnames = [
            "Case_ID",
            "Activity",
            "Timestamp"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(events)

    print(f"Dataset created successfully: {output_file}")
    print(f"Total events generated: {len(events)}")


if __name__ == "__main__":

    events = generate_dataset()

    save_to_csv(events)