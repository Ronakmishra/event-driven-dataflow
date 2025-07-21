from datetime import datetime
import json

def app(event, context):
    print("Received event:", json.dumps(event))

    filtered_records = []

    for record in event.get("records", []):
        data = record.get("record", {})
        start = datetime.strptime(data["startDate"], "%Y-%m-%d")
        end = datetime.strptime(data["endDate"], "%Y-%m-%d")
        duration = (end - start).days

        if duration > 1:
            data["bookingDuration"] = duration
            filtered_records.append(record)

    return {"records": filtered_records}
