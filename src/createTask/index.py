import json
import boto3
import uuid
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    try:
        body = json.loads(event["body"])
        task_id = str(uuid.uuid4())
        task_item = {
            "id": task_id,
            "title": body.get("title"),
            "description": body.get("description"),
            "assignedTo": body.get("assignedTo"),
            "status": "pending"
        }

        table.put_item(Item=task_item)

        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            },
            "body": json.dumps({"message": "Task created", "taskId": task_id})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            },
            "body": json.dumps({
                "message": "Internal server error",
                "error": str(e)
            })
        }
