import json

def handler(event: dict, context: dict) -> dict:
    return {
        "statusCode": 403,
        "body": json.dumps({"message": "Forbidden"})
    }
