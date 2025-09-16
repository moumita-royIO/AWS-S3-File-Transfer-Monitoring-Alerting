# Lambda for missing file alerts (S3 event-driven)

import os
import boto3
from helper import send_email

s3 = boto3.client("s3")

BUCKET = os.environ.get("BUCKET_NAME")
OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
if not BUCKET:
    raise ValueError("BUCKET_NAME environment variable is not set")

# Predefine the expected files

EXPECTED_FILES = [
    "Indoor_daily.csv",   
    "Outdoor_daily.csv" 
]

def lambda_handler(event, context):
    """
    Triggered by S3 ObjectCreated:* event.
    Sends immediate alert if an expected file is missing.
    """
    for record in event["Records"]:
        key = record["s3"]["object"]["key"]
        print(f"File uploaded: {key}")

    # Check for missing expected files
    missing_files = []
    for file_key in EXPECTED_FILES:
        try:
            s3.head_object(Bucket=BUCKET, Key=file_key)
        except s3.exceptions.ClientError:
            missing_files.append(file_key)

    if missing_files:
        subject = "Immediate S3 Missing File Alert"
        body = "The following expected files are missing:\n" + "\n".join(missing_files)
        send_email(subject, body)
        print("Immediate alert sent for missing files:", missing_files)
    else:
        print("All expected files are present.")
