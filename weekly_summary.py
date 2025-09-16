import os
import boto3
from botocore.exceptions import ClientError

# Environment variables
BUCKET = os.environ.get("BUCKET_NAME")
OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
MIN_SIZE = int(os.environ.get("MIN_SIZE", 100 * 1024))  # default 100 KB

if not BUCKET or not OWNER_EMAIL:
    raise ValueError("BUCKET_NAME and OWNER_EMAIL environment variables must be set")

# AWS clients
s3 = boto3.client("s3")
ses = boto3.client("ses")


def send_email(subject, body):
    try:
        ses.send_email(
            Source=OWNER_EMAIL,
            Destination={"ToAddresses": [OWNER_EMAIL]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}}
            }
        )
        print("Email sent successfully")
    except ClientError as e:
        print(f"Error sending email: {e}")


def lambda_handler(event, context):
    try:
        response = s3.list_objects_v2(Bucket=BUCKET)
        objects = response.get("Contents", [])

        if not objects:
            print(f"No files found in bucket {BUCKET}")
            return

        # Collect small files
        small_files = []
        for obj in objects:
            key = obj['Key']
            size = obj['Size']
            print(f"File: {key} Size: {size} bytes")
            if size < MIN_SIZE:
                small_files.append(f"{key} ({size} bytes)")

        # Send SES email if there are small files
        if small_files:
            subject = f"S3 Weekly Summary: Files smaller than {MIN_SIZE} bytes"
            body = "The following files are smaller than the minimum size:\n\n" + "\n".join(small_files)
            send_email(subject, body)
        else:
            print("All files meet the minimum size requirement.")

    except ClientError as e:
        print(f"Error listing objects in bucket {BUCKET}: {e}")
