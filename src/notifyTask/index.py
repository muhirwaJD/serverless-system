import json
import boto3
import os

sns = boto3.client("sns")
topic_arn = os.environ["TOPIC_ARN"]

def handler(event, context):
    try:
        body = json.loads(event["body"])
        message = body.get("message", "This is a task reminder.")

        sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject="Task Reminder"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Reminder sent"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error sending reminder", "error": str(e)})
        }
