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
        expr_attr_names = {}
        
        # Handle regular fields and reserved keywords
        field_mappings = {
            "title": "title",
            "description": "description", 
            "assignedTo": "assignedTo",
            "status": "#status"  # Use expression attribute name for reserved keyword
        }
        
        for key in field_mappings:
            if key in body:
                attr_name = field_mappings[key]
                if key == "status":
                    # Handle reserved keyword
                    expr_attr_names["#status"] = "status"
                    update_expr += f"#status = :{key}, "
                else:
                    update_expr += f"{attr_name} = :{key}, "
                expr_attr_values[f":{key}"] = body[key]

        update_expr = update_expr.rstrip(", ")

        if not expr_attr_values:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "PUT, OPTIONS"
                },
                "body": json.dumps({"message": "No valid fields to update"})
            }

        # Build update_item parameters
        update_params = {
            "Key": {"id": task_id},
            "UpdateExpression": update_expr,
            "ExpressionAttributeValues": expr_attr_values
        }
        
        # Only add ExpressionAttributeNames if we have reserved keywords
        if expr_attr_names:
            update_params["ExpressionAttributeNames"] = expr_attr_names

        table.update_item(**update_params)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "PUT, OPTIONS"
            },
            "body": json.dumps({"message": "Task updated successfully"})
        }

    except Exception as e:
        print("Update task failed:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "PUT, OPTIONS"
            },
            "body": json.dumps({"message": "Error updating task", "error": str(e)})
        }
