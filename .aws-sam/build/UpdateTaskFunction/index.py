import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    try:
        task_id = event["pathParameters"]["id"]
        body = json.loads(event["body"])

        update_expr = "SET "
        expr_attr_values = {}
        for key in ["title", "description", "assignedTo", "status"]:
            if key in body:
                update_expr += f"{key} = :{key}, "
                expr_attr_values[f":{key}"] = body[key]

        update_expr = update_expr.rstrip(", ")

        if not expr_attr_values:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "No valid fields to update"})
            }

        table.update_item(
            Key={"id": task_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_attr_values
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Task updated"})
        }

    except Exception as e:
        print("Update task failed:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error updating task", "error": str(e)})
        }
