import boto3
import os
import json
import uuid
import random
from datetime import datetime, timedelta

sqs = boto3.client('sqs')
QUEUE_URL = os.getenv("QUEUE_URL")

def generate_mock_booking():
    cities = ["NYC", "Chicago", "San Francisco", "Austin", "Miami"]
    bookings = []
    for i in range(6):
        start = datetime.today() + timedelta(days=random.randint(0, 10))
        end = start + timedelta(days=random.randint(1, 7))
        booking = {
            "bookingId": str(uuid.uuid4()),
            "userId": f"U{random.randint(100, 999)}",
            "propertyId": f"P{random.randint(1000, 9999)}",
            "location": random.choice(cities),
            "startDate": start.strftime("%Y-%m-%d"),
            "endDate": end.strftime("%Y-%m-%d"),
            "price": round(random.uniform(100, 1000), 2)
        }
        bookings.append(booking)
    return bookings

def lambda_handler(event, context):
    for booking in generate_mock_booking():
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(booking)
        )
        print(f"Sent: {booking['bookingId']}")

    return {
        "statusCode": 200,
        "body": "Mock bookings sent"
    }
