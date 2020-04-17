import os
import json
import boto3
from serverless_sdk import tag_event

SENDER = os.getenv("SENDER")
RECEIVER = os.getenv("RECEIVER")

mailer = boto3.client("ses")


def contact(event, context):
    tag_event("custom-tag", "contact-form", {"custom": {"tag": "data "}})

    print(event)
    data = json.loads(event.get("body"))
    full_name, email = data.get("FullName"), data.get("Email")
    subject, message = data.get("Subject"), data.get("Message")

    mailer.send_email(
        Source=SENDER,
        Destination={"ToAddresses": [RECEIVER]},
        Message={
            "Subject": {"Data": f"[Site] {subject}", "Charset": "utf-8"},
            "Body": {
                "Text": {
                    "Data": "Message from: {}, email: {}:\n---\n{}".format(
                        full_name, email, message
                    ),
                    "Charset": "utf-8",
                }
            },
        },
    )

    headers = {
        "Access-Control-Allow-Origin": "*",
    }

    body = {
        "message": "Thank you for your email",
    }

    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}

    return response
