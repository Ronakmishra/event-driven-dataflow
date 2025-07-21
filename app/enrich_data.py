from datetime import datetime
import json

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    filtered_records = []
    
    # Handle different event formats
    if isinstance(event, dict) and "Records" in event:
        # Standard SQS event format
        for sqs_record in event["Records"]:
            booking_data = json.loads(sqs_record["body"])
            process_booking(booking_data, filtered_records)
    
    elif isinstance(event, list):
        # EventBridge Pipe format - list of messages
        for message in event:
            # EventBridge Pipe sends the SQS message structure
            if "body" in message:
                # Parse the body which contains the booking data
                booking_data = json.loads(message["body"])
            else:
                # Direct booking data
                booking_data = message
            
            process_booking(booking_data, filtered_records)
    
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

def process_booking(booking_data, filtered_records):
    """Process a single booking and add to filtered_records if duration > 1"""
    try:
        start = datetime.strptime(booking_data["startDate"], "%Y-%m-%d")
        end = datetime.strptime(booking_data["endDate"], "%Y-%m-%d")
        duration = (end - start).days
        
        if duration > 1:
            booking_data["bookingDuration"] = duration
            filtered_records.append(booking_data)
            print(f"Added booking {booking_data.get('bookingId')} with duration {duration} days")
    except KeyError as e:
        print(f"Missing key in booking data: {e}")
        print(f"Booking data: {json.dumps(booking_data)}")
    except Exception as e:
        print(f"Error processing booking: {e}")
        print(f"Booking data: {json.dumps(booking_data)}")