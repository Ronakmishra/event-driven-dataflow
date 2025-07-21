from datetime import datetime
import json

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    filtered_records = []
    
    # Handle different event formats
    if isinstance(event, dict) and "Records" in event:
        # SQS event format
        for sqs_record in event["Records"]:
            # Parse the SQS message body which contains the actual booking data
            booking_data = json.loads(sqs_record["body"])
            
            # Process the booking data
            start = datetime.strptime(booking_data["startDate"], "%Y-%m-%d")
            end = datetime.strptime(booking_data["endDate"], "%Y-%m-%d")
            duration = (end - start).days
            
            if duration > 1:
                booking_data["bookingDuration"] = duration
                filtered_records.append(booking_data)
    
    elif isinstance(event, list):
        # Direct invocation with list of bookings
        for booking_data in event:
            start = datetime.strptime(booking_data["startDate"], "%Y-%m-%d")
            end = datetime.strptime(booking_data["endDate"], "%Y-%m-%d")
            duration = (end - start).days
            
            if duration > 1:
                booking_data["bookingDuration"] = duration
                filtered_records.append(booking_data)
    
    else:
        print(f"Unexpected event format: {type(event)}")
    
    # Return the filtered records
    return {
        "statusCode": 200,
        "body": json.dumps({
            "filteredCount": len(filtered_records),
            "records": filtered_records
        })
    }