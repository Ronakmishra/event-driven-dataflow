import boto3
import csv
import json
import os
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = os.getenv("TARGET_BUCKET")

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    records = []
    
    # Handle different event formats from EventBridge Pipe
    if isinstance(event, list):
        # EventBridge might send a list of enrichment responses
        for item in event:
            if isinstance(item, dict):
                # Check if it's the Lambda response format
                if "statusCode" in item and "body" in item:
                    # Parse the Lambda response body
                    body = json.loads(item["body"]) if isinstance(item["body"], str) else item["body"]
                    records.extend(body.get("records", []))
                elif "records" in item:
                    # Direct records format
                    records.extend(item["records"])
                else:
                    # Assume it's a booking record
                    records.append(item)
    
    elif isinstance(event, dict):
        # Single response object
        if "statusCode" in event and "body" in event:
            # Lambda response format
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
            records = body.get("records", [])
        elif "records" in event:
            # Direct records access
            records = event["records"]
        else:
            print("No records found in dict event")
            return {"statusCode": 204, "body": "No records to process"}
    
    else:
        print(f"Unexpected event type: {type(event)}")
        return {"statusCode": 400, "body": "Invalid event format"}
    
    if not records:
        return {"statusCode": 204, "body": "No records to process"}
    
    # Generate CSV
    csv_key = f"transformed_output/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    csv_data = [["bookingId", "userId", "location", "startDate", "endDate", "price", "bookingDuration"]]
    
    for record in records:
        # Each record should be a booking object
        csv_data.append([
            record.get("bookingId"),
            record.get("userId"),
            record.get("location"),
            record.get("startDate"),
            record.get("endDate"),
            record.get("price"),
            record.get("bookingDuration", "")  # Include duration if available
        ])
    
    # Upload to S3
    csv_content = "\n".join([",".join(map(str, row)) for row in csv_data])
    
    response = s3.put_object(
        Bucket=BUCKET,
        Key=csv_key,
        Body=csv_content
    )
    
    print(f"File uploaded: {csv_key}")
    print(f"Processed {len(records)} records")
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Transformation complete",
            "recordsProcessed": len(records),
            "s3Key": csv_key
        })
    }