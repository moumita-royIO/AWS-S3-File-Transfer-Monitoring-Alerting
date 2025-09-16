# Shared helper functions (SES email, logging)

import boto3
import os

ses = boto3.client("ses")
MIN_SIZE = 100 * 1024  # 100 KB
OWNER_EMAIL = os.environ["OWNER_EMAIL"]

def send_email(subject, body):
    """Send email via SES."""
    ses.send_email(
        Source=OWNER_EMAIL,
        Destination={"ToAddresses": [OWNER_EMAIL]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}}
        }
    )

def is_file_too_small(size):
    """Check if file is smaller than minimum size."""
    return size < MIN_SIZE
