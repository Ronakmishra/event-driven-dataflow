import boto3
import csv
import json
import os
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = os.getenv("TARGET_BUCKET")

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    records = [record["body"] for record in event.get("records", [])]
    data = [json.loads(r) for r in records]

    if not data:
        return {"statusCode": 204, "body": "No records to process"}

    csv_key = f"transformed_output/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    csv_data = [["bookingId", "userId", "location", "startDate", "endDate", "price"]]

    for row in data:
        csv_data.append([
            row.get("bookingId"),
            row.get("userId"),
            row.get("location"),
            row.get("startDate"),
            row.get("endDate"),
            row.get("price")
        ])

    response = s3.put_object(
        Bucket=BUCKET,
        Key=csv_key,
        Body="\n".join([",".join(map(str, row)) for row in csv_data])
    )

    print("File uploaded:", csv_key)
    return {"statusCode": 200, "body": "Transformation complete"}
