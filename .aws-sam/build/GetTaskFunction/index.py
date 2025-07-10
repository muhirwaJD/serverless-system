import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    try:
        response = table.scan()
        tasks = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps(tasks)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error retrieving tasks", "error": str(e)})
        }
