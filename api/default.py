import json

def handler(event, context):
    return {
        "statusCode": 403,
        "body": json.dumps({"error_msg": "Forbidden"})
    }
