from datetime import datetime
import json

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    filtered_records = []
    
    # When triggered by SQS, event contains 'Records' (capital R)
    for sqs_record in event.get("Records", []):
        # Parse the SQS message body which contains the actual booking data
        booking_data = json.loads(sqs_record["body"])
        
        # Now process the booking data
        start = datetime.strptime(booking_data["startDate"], "%Y-%m-%d")
        end = datetime.strptime(booking_data["endDate"], "%Y-%m-%d")
        duration = (end - start).days
        
        if duration > 1:
            booking_data["bookingDuration"] = duration
            filtered_records.append(booking_data)
    
    # Return the filtered records
    return {
        "statusCode": 200,
        "body": json.dumps({
            "filteredCount": len(filtered_records),
            "records": filtered_records
        })
    }